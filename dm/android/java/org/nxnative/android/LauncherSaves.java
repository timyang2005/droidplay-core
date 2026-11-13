// The Save rows of a game's settings screen (Launcher.java): Export save writes the game's save as a ZIP, Import save takes one from a ZIP or a folder, Earlier
// saves puts back a save kept before an import or by Back up saves. Through Android's file picker (the Storage Access Framework), so the player picks where a save
// goes or comes from (Downloads, a cloud drive, an SD card) and the app needs no storage permission. Saves.java finds the save and swaps it in; this file is the
// screens and the copying to and from the picker.
//   Import: a ZIP is copied to the cache first (ZipFile reads its central directory, which a stream can't), a folder walked through DocumentsContract; either is
//   staged in internal files/import-staging/, Saves.find looks for saves there, the player picks one when there are several and confirms what it is. The game's
//   save is then copied to <external files>/backups/<time>-<title ID>/ (a backup as Back up saves writes one, so the desktop app's backup copies it too) and the new
//   one swapped in. Never while the game runs: its host would commit its own save over the new one, so the player is asked to close it first.
package org.nxnative.android;

import android.app.AlertDialog;
import android.content.ContentResolver;
import android.content.DialogInterface;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.provider.DocumentsContract;
import android.provider.DocumentsContract.Document;
import android.provider.OpenableColumns;
import android.system.Os;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Locale;

final class LauncherSaves {
    static final int EXPORT = 21, IMPORT_FILE = 22, IMPORT_FOLDER = 23;
    static final int DIALOG = android.R.style.Theme_DeviceDefault_Dialog_Alert;
    static final String PREF = "save_for";   // the game a picker was opened for: the launcher may be recreated while the picker is up
    // the user namespace alone (the host's guest names, plat_android.c xname): a file's security.selinux names this app's own categories, which an import from
    // another phone or app must not carry
    static final Saves.Xattrs XA = new Saves.Xattrs() {
        public void read(File f, String rel, StringBuilder tsv) {
            try { for (String n : Os.listxattr(f.getPath())) if (n.startsWith("user.")) tsv.append(rel).append('\t').append(n).append('\t').append(Launcher.hex(Os.getxattr(f.getPath(), n))).append('\n'); }
            catch (Exception e) { /* a file system without xattrs */ }
        }
        public void apply(File root, String top, File tsv) { Launcher.applyXattrs(root, top, Launcher.readXattrs(tsv)); }
    };
    final Launcher l; volatile boolean busy; AlertDialog progress;
    File source; boolean computer;   // what the save on show came in (the staging folder, or an import/<title ID> folder), deleted when its dialogs end; whether a computer sent it
    LauncherSaves(Launcher l) { this.l = l; }

    File saves() { return new File(l.internal, "saves"); }
    File backups() { return new File(l.ext, "backups"); }
    File staging() { return new File(l.internal, "import-staging"); }
    ContentResolver cr() { return l.getContentResolver(); }
    boolean hasSave(String id) { return Saves.hasFiles(new File(saves(), id)) || Saves.hasFiles(new File(saves(), id + "_device")); }

    // ---------------- the rows ----------------
    View rows(final Launcher.Game g) {
        LinearLayout box = new LinearLayout(l); box.setOrientation(LinearLayout.VERTICAL);
        TextView h = l.caps(Loc.t("Save", "存档")); h.setPadding(0, l.px(18), 0, l.px(6)); box.addView(h);
        box.addView(row(Loc.t("Export save", "导出存档"), Loc.t("A zip of the save, to keep, or to take to another phone or an emulator.", "一份存档的 zip：留着备份，或带去别的手机、别的模拟器。"), Loc.t("Export…", "导出…"), new Runnable() { public void run() { export(g); } }));
        box.addView(row(Loc.t("Import save", "导入存档"), Loc.t("From a zip or a folder: a DroidPlay export, Ryujinx's or a yuzu-family emulator's save folder, JKSV, EdiZon, Checkpoint, or a PC port's. The save here is kept first.",
            "来自 zip 或文件夹：DroidPlay 导出的、Ryujinx 或 yuzu 系模拟器的存档目录、JKSV、EdiZon、Checkpoint，或者 PC 移植版的。这里现有的存档会先保留。"), Loc.t("Import…", "导入…"), new Runnable() { public void run() { importAsk(g); } }));
        box.addView(row(Loc.t("Earlier saves", "更早的存档"), Loc.t("The saves kept before an import, and Back up saves' copies.", "导入前保留的存档，以及「备份存档」留下的副本。"), Loc.t("Restore…", "恢复…"), new Runnable() { public void run() { restoreAsk(g); } }));
        return box;
    }
    View row(String label, String note, String button, final Runnable go) {
        LinearLayout r = new LinearLayout(l); r.setGravity(Gravity.CENTER_VERTICAL); r.setMinimumHeight(l.px(48)); r.setPadding(0, l.px(6), 0, l.px(6));
        LinearLayout words = new LinearLayout(l); words.setOrientation(LinearLayout.VERTICAL);
        words.addView(l.text(label, 14, Launcher.TEXT, 400));
        TextView t = l.text(note, 11, Launcher.TEXT2, 400); t.setPadding(0, l.px(2), l.px(12), 0); t.setLineSpacing(0, 1.2f); words.addView(t);
        r.addView(words, new LinearLayout.LayoutParams(0, -2, 1));
        TextView b = l.pill(button, Launcher.LIFT, Launcher.TEXT);
        b.setOnClickListener(new View.OnClickListener() { public void onClick(View v) { if (!busy) go.run(); } });
        r.addView(b, new LinearLayout.LayoutParams(-2, l.px(36)));
        return r;
    }

    // The game closed first when it is running, after asking, then go: its host commits its save at its own times and would put it back over the new one
    void whenClosed(final Launcher.Game g, String doing, final Runnable go) {
        String running = l.runningGame();
        if (running == null || !running.equalsIgnoreCase(g.id)) { go.run(); return; }
        new AlertDialog.Builder(l, DIALOG).setTitle(Loc.f("%s is running", "%s 正在运行", g.name))
            .setMessage(Loc.f("Close it to %s? Progress it has not saved is lost.", "关掉它才能%s，继续吗？它没保存的进度会丢失。", doing))
            .setPositiveButton(Loc.t("Close it", "关掉它"), new DialogInterface.OnClickListener() { public void onClick(DialogInterface d, int w) { l.endGame(); l.ui.postDelayed(go, 600); } })
            .setNegativeButton(Loc.t("Cancel", "取消"), null).show();
    }
    void pick(Launcher.Game g, Intent i, int req) {
        l.app.edit().putString(PREF, g.id).apply();
        try { l.startActivityForResult(i, req); }
        catch (android.content.ActivityNotFoundException e) { info(Loc.t("No file picker", "没有文件选择器"), Loc.f("This phone has no app that picks files: %s", "这台手机没有能选文件的应用：%s", e.getMessage())); }
    }

    // ---------------- export ----------------
    void export(final Launcher.Game g) {
        if (!hasSave(g.id)) { info(Loc.t("No save yet", "还没有存档"), Loc.f("%s has no save on this phone yet: play it until it saves, then export it.", "%s 在这台手机上还没有存档：玩到它存一次档，再来导出。", g.name)); return; }
        whenClosed(g, Loc.t("export its save", "导出存档"), new Runnable() { public void run() {
            Intent i = new Intent(Intent.ACTION_CREATE_DOCUMENT).addCategory(Intent.CATEGORY_OPENABLE).setType("application/zip")
                .putExtra(Intent.EXTRA_TITLE, fileName(g.name) + Loc.t(" save ", " 存档 ") + new SimpleDateFormat("yyyy-MM-dd HHmm", Locale.ROOT).format(new Date()) + ".zip");
            pick(g, i, EXPORT);
        } });
    }
    void exportTo(final Launcher.Game g, final Uri uri) {
        working(Loc.f("Exporting %s's save…", "正在导出 %s 的存档…", g.name), new Runnable() { public void run() {
            String readme = Loc.f("DroidPlay save export: %s (%s)%s, %s.\n\n", "DroidPlay 存档导出：%s（%s）%s，%s。\n\n", g.name, g.id, g.version != null ? Loc.f(", version %s", "，版本 %s", g.version) : "", now())
                + Loc.f("saves/%s/ holds the save as the game sees it, and saves/%s_device/ its device save, for a game that has both. DroidPlay imports this zip as it is (the game's screen > Import save). For an emulator, copy the files inside saves/%s/ into its save folder for this game.\n",
                    "saves/%s/ 里是游戏看到的那份存档，saves/%s_device/ 是它的设备存档（两者都有的游戏才有）。DroidPlay 原样导入这个 zip（游戏的设置页 > 导入存档）。要拿去别的模拟器用，把 saves/%s/ 里的文件复制到它这个游戏的存档文件夹。\n", g.id, g.id, g.id)
                + Loc.t("xattrs.tsv: the files' extended attributes, which DroidPlay puts back.\n", "xattrs.tsv：这些文件的扩展属性，DroidPlay 会一并放回去。\n");
            try (OutputStream o = cr().openOutputStream(uri, "w")) {
                if (o == null) throw new IOException(Loc.t("the place picked can't be written", "选的位置写不进去"));
                int n = Saves.export(l.internal, g.id, o, readme, XA);
                Log.i(Launcher.TAG, "save of " + g.id + " exported: " + n + " files to " + uri);
                done(Loc.t("Save exported", "存档已导出"), Loc.f("%s's save (%d files) is in %s.", "%s 的存档（%d 个文件）在 %s。", g.name, n, name(uri)));
            } catch (Exception e) {
                Log.w(Launcher.TAG, "export: " + e);
                try { DocumentsContract.deleteDocument(cr(), uri); } catch (Exception gone) { /* the provider keeps it, or it is gone */ }
                done(Loc.t("Export failed", "导出失败"), Loc.f("The save couldn't be written: %s", "存档写不进去：%s", e.getMessage()));
            }
        } });
    }

    // ---------------- import ----------------
    void importAsk(final Launcher.Game g) {
        whenClosed(g, Loc.t("import a save", "导入存档"), new Runnable() { public void run() {
            new AlertDialog.Builder(l, DIALOG).setTitle(Loc.f("Import a save for %s", "为 %s 导入存档", g.name))
                .setItems(new String[] {Loc.t("From a zip file", "从 zip 文件"), Loc.t("From a folder", "从文件夹")}, new DialogInterface.OnClickListener() { public void onClick(DialogInterface d, int w) {
                    if (w == 0) pick(g, new Intent(Intent.ACTION_OPEN_DOCUMENT).addCategory(Intent.CATEGORY_OPENABLE).setType("*/*"), IMPORT_FILE);
                    else pick(g, new Intent(Intent.ACTION_OPEN_DOCUMENT_TREE), IMPORT_FOLDER);
                } }).setNegativeButton(Loc.t("Cancel", "取消"), null).show();
        } });
    }
    void staged(final Launcher.Game g, final Uri uri, final boolean folder) {
        working(Loc.t("Reading what you picked…", "正在读取你选的内容…"), new Runnable() { public void run() {
            File st = staging(); Saves.deleteTree(st); st.mkdirs(); String why;
            long limit = Math.min(8L << 30, l.internal.getUsableSpace() / 3);   // the copy here, the copy beside the save, and room left
            try { why = folder ? stageFolder(uri, st, limit) : stageFile(uri, st, limit); }
            catch (Exception e) { Log.w(Launcher.TAG, "import: " + e); why = String.valueOf(e.getMessage()).startsWith("too big") ? Loc.t("It's bigger than this phone has room for.", "它比这台手机能腾出的空间还大。") : Loc.f("It can't be read: %s", "读不了：%s", e.getMessage()); }
            if (why != null) { Saves.deleteTree(st); done(Loc.t("Nothing imported", "没有导入任何东西"), why); return; }
            final List<Saves.Found> fs = Saves.find(st, g.id, Saves.names(new File(saves(), g.id)), Saves.names(new File(saves(), g.id + "_device")));
            then(new Runnable() { public void run() { source = staging(); computer = false; choose(g, fs); } });
        } });
    }
    String stageFile(Uri uri, File st, long limit) throws IOException {
        File zip = new File(l.getCacheDir(), "import.zip"); String name = name(uri);
        try {
            try (InputStream in = cr().openInputStream(uri)) { if (in == null) throw new IOException(Loc.t("the file can't be opened", "这个文件打不开")); copy(in, zip, limit); }
            String kind = Saves.kind(Saves.head(zip, 8));
            if (kind == null) return Loc.f("%s isn't a zip. Pick a zip of the save, or the folder that holds its files (From a folder).", "%s 不是 zip。请选存档的 zip，或装着它文件的文件夹（「从文件夹」）。", name);
            if (!kind.equals("zip")) return Loc.f("%s archives can't be opened on a phone: unpack %s first (with a file manager app, or on a computer), then import its folder.", "%s 压缩包在手机上打不开：先用手机上的文件管理器、或在电脑上把 %s 解压，再导入它的文件夹。", kind, name);
            try { Saves.unzip(zip, st, limit); }
            catch (IOException e) {
                String m = String.valueOf(e.getMessage());
                if (m.startsWith("method ")) return Loc.f("%s is packed with a compression Android can't unpack (%s): unpack it with a file manager app or on a computer, then import its folder.",
                    "%s 用的压缩方式 Android 解不开（%s）：用文件管理器应用或电脑解压，再导入它的文件夹。", name, m.equals("method 9") ? Loc.t("Deflate64, which Windows uses for big zips" , "Deflate64，Windows 压大 zip 用的就是它") : m);
                throw e;
            }
            return null;
        } finally { zip.delete(); }
    }
    // The folder picked → st/<its name>/, so that its name (a title ID, a Ryujinx save ID, a dated backup) is there for Saves.find
    String stageFolder(Uri tree, File st, long limit) throws IOException {
        String id = DocumentsContract.getTreeDocumentId(tree);
        String name = name(DocumentsContract.buildDocumentUriUsingTree(tree, id));
        if (name == null || name.isEmpty() || name.contains("/") || name.startsWith(".")) name = "picked";
        long[] left = {limit}; int[] n = {0};
        walk(tree, id, new File(st, name), left, n, 0);
        return n[0] == 0 ? Loc.f("The folder %s holds no files.", "文件夹 %s 里没有文件。", name) : null;
    }
    void walk(Uri tree, String id, File dst, long[] left, int[] n, int depth) throws IOException {
        if (depth > 16) return;
        if (!dst.isDirectory() && !dst.mkdirs()) throw new IOException(Loc.f("can't make %s", "建不了 %s", dst));
        String[] cols = {Document.COLUMN_DOCUMENT_ID, Document.COLUMN_DISPLAY_NAME, Document.COLUMN_MIME_TYPE, Document.COLUMN_LAST_MODIFIED};
        try (Cursor c = cr().query(DocumentsContract.buildChildDocumentsUriUsingTree(tree, id), cols, null, null, null)) {
            if (c == null) throw new IOException(Loc.t("the folder can't be listed", "这个文件夹列不出来"));
            while (c.moveToNext()) {
                String kid = c.getString(0), name = c.getString(1), mime = c.getString(2);
                if (name == null || name.isEmpty() || name.equals(".") || name.equals("..") || name.contains("/") || Saves.junk(name)) continue;
                File out = new File(dst, name);
                if (Document.MIME_TYPE_DIR.equals(mime)) { walk(tree, kid, out, left, n, depth + 1); continue; }
                try (InputStream in = cr().openInputStream(DocumentsContract.buildDocumentUriUsingTree(tree, kid))) {
                    if (in == null) throw new IOException(Loc.f("%s can't be opened", "%s 打不开", name));
                    left[0] -= copy(in, out, left[0]);
                }
                if (!c.isNull(3) && c.getLong(3) > 0) out.setLastModified(c.getLong(3));   // the save's own times, for the player to tell saves apart
                if (++n[0] % 50 == 0) say(Loc.f("Reading what you picked… %d files", "正在读取你选的内容… %d 个文件", n[0]));
            }
        }
    }

    void choose(final Launcher.Game g, final List<Saves.Found> fs) {
        if (fs.isEmpty()) {
            cleanup();
            info(Loc.t("No save found", "没找到存档"), Loc.f("Nothing in %s looks like a save. Pick the folder that holds the save's files, or a zip of it: for an emulator, the folder its \"Open save data location\" opens, or the one above it.",
                "%s 里没有像存档的东西。请选装着存档文件的文件夹，或它的 zip；模拟器的话，就是它「打开存档数据位置」打开的那个文件夹，或者它的上一层。",
                computer ? Loc.t("what your computer sent", "电脑发来的内容") : Loc.t("what you picked", "你选的内容")));
            return;
        }
        if (fs.size() == 1) { confirm(g, fs.get(0)); return; }
        String[] items = new String[fs.size()];
        for (int i = 0; i < items.length; i++) items[i] = what(fs.get(i)) + "\n" + size(fs.get(i));
        new AlertDialog.Builder(l, DIALOG).setTitle(computer ? Loc.f("Which save from your computer, for %s?", "用电脑上的哪份存档给 %s？", g.name) : Loc.t("Which save?", "哪份存档？"))
            .setItems(items, new DialogInterface.OnClickListener() { public void onClick(DialogInterface d, int w) { confirm(g, fs.get(w)); } })
            .setNegativeButton(Loc.t("Cancel", "取消"), new DialogInterface.OnClickListener() { public void onClick(DialogInterface d, int w) { cleanup(); } })
            .setCancelable(false).show();
    }
    void confirm(final Launcher.Game g, final Saves.Found f) {
        boolean other = f.titleId != null && !f.titleId.equalsIgnoreCase(g.id);
        StringBuilder m = new StringBuilder(what(f)).append('\n').append(size(f)).append(Loc.t("\nIt holds: ", "\n内容：")).append(top(f.main(), 6)).append('\n');
        if (other) m.append(Loc.f("\nThis is the save of another game: %s (%s). It won't load in %s unless that is the same game from another region.\n", "\n这是另一个游戏的存档：%s（%s）。除非它是同一个游戏的其他区版本，否则 %s 载入不了。\n", l.nameOf(f.titleId), f.titleId, g.name));
        else if (f.titleId == null && !f.matched) m.append(Loc.f("\nThese files don't say which game they're from: check that they're %s's.\n", "\n这些文件没说是哪个游戏的：请确认它们是 %s 的。\n", g.name));
        if (f.matched) m.append(Loc.f("\nTheir names match %s's save on this phone.\n", "\n它们的文件名和这台手机上 %s 的存档对得上。\n", g.name));
        else if (f.unmatched) m.append(Loc.f("\nThey share no names with %s's save on this phone, which holds %s.\n", "\n它们和这台手机上 %s 的存档没有一个同名文件，那份存档里是 %s。\n", g.name, top(new File(saves(), g.id), 4)));
        if (g.version != null) m.append(Loc.f("\nThe game here is version %s: a save from a later update may not load.\n", "\n这里的游戏是版本 %s：更晚的更新存下的存档可能载入不了。\n", g.version));
        m.append('\n').append(hasSave(g.id) ? Loc.f("The save %s has now is kept first: Earlier saves > Restore puts it back.", "%s 现在的存档会先保留：「更早的存档 > 恢复」可以把它放回去。", g.name) : Loc.f("%s has no save on this phone yet.", "%s 在这台手机上还没有存档。", g.name));
        new AlertDialog.Builder(l, DIALOG).setTitle(computer ? Loc.t("Import this save from your computer?", "从电脑导入这份存档吗？") : Loc.t("Import this save?", "导入这份存档吗？"))
            .setMessage((computer ? Loc.f("For %s: ", "给 %s：", g.name) : "") + m)
            .setPositiveButton(other ? Loc.t("Import anyway", "仍然导入") : Loc.t("Import", "导入"), new DialogInterface.OnClickListener() { public void onClick(DialogInterface d, int w) { install(g, f, false); } })
            .setNegativeButton(Loc.t("Cancel", "取消"), new DialogInterface.OnClickListener() { public void onClick(DialogInterface d, int w) { cleanup(); } })
            .setCancelable(false).show();
    }

    // The game's save kept, then f swapped in. restoring: f is a kept save (Earlier saves), not the staged import
    void install(final Launcher.Game g, final Saves.Found f, final boolean restoring) {
        final String running = l.runningGame();
        if (running != null && running.equalsIgnoreCase(g.id)) {   // started from the desktop app while the picker was up
            if (!restoring) cleanup();
            info(Loc.t("Nothing imported", "没有导入任何东西"), Loc.f("%s is running: close it, then try again.", "%s 正在运行：关掉它再试一次。", g.name)); return;
        }
        working(restoring ? Loc.t("Putting the save back…", "正在放回存档…") : Loc.t("Importing the save…", "正在导入存档…"), new Runnable() { public void run() {
            File keep = new File(backups(), new SimpleDateFormat("yyyyMMdd-HHmmss", Locale.ROOT).format(new Date()) + "-" + g.id);
            boolean kept;
            try {
                kept = Saves.keep(l.internal, g.id, keep, Loc.f("DroidPlay save backup: %s (%s)'s save before %s, %s.\nThe game's screen in DroidPlay > Earlier saves > Restore puts it back; so does copying this folder to backups/restore/ on the phone.\n",
                    "DroidPlay 存档备份：%s（%s）在%s之前的存档，%s。\n在 DroidPlay 该游戏的设置页用「更早的存档 > 恢复」就能放回去；把这个文件夹复制到手机上的 backups/restore/ 也可以。\n",
                    g.name, g.id, restoring ? Loc.t("a restore", "恢复") : Loc.t("an import", "导入"), now()), XA);
            } catch (IOException e) {
                Saves.deleteTree(keep); if (!restoring) cleanup();
                done(Loc.t("Nothing imported", "没有导入任何东西"), Loc.f("The save %s has now couldn't be kept first (%s), so it was left as it is. Free some space and try again.", "%s 现在的存档没能先保留（%s），所以它原样没动。腾出一些空间再试。", g.name, e.getMessage()));
                return;
            }
            try {
                Saves.install(l.internal, g.id, f, XA);
                Log.i(Launcher.TAG, "save of " + g.id + (restoring ? " restored from " : " imported from ") + f.format + " " + f.label + " (" + f.files + " files)" + (kept ? "; the one before is in " + keep : ""));
                done(restoring ? Loc.t("Save restored", "存档已恢复") : Loc.t("Save imported", "存档已导入"), Loc.f("%s starts from it next time: pick Continue, or load it in the game.", "%s 下次从这份存档开始：在游戏里选「继续」，或读取它。", g.name)
                    + (kept ? Loc.t("\n\nThe save it had is kept: Earlier saves > Restore puts it back.", "\n\n它原来那份存档已保留：「更早的存档 > 恢复」可以放回去。") : ""));
            } catch (IOException e) {
                Log.w(Launcher.TAG, "install: " + e);
                done(Loc.t("Import failed", "导入失败"), Loc.f("The save couldn't be swapped in (%s).", "存档换不进去（%s）。", e.getMessage())
                    + (kept ? Loc.f(" The one %s had is kept: Earlier saves > Restore puts it back.", " %s 原来那份已保留：「更早的存档 > 恢复」可以放回去。", g.name) : ""));
            } finally { if (!restoring) cleanup(); }
        } });
    }

    // The save's folder gone once its dialogs end. An import/<title ID> folder the app can't delete (adb made it, and its chmod was cut short) is remembered by its
    // time, so it isn't offered at every start
    void cleanup() {
        File f = source; source = null; if (f == null) return;
        Saves.deleteTree(f);
        if (f.exists() && computer) l.app.edit().putLong(SEEN + f.getName(), f.lastModified()).apply();
    }

    // ---------------- from the computer ----------------
    // A save the desktop app or the command line sent (scripts/build_android_from_nsp.py --import-save / --restore-backup): adb can't write the app's internal storage,
    // so it pushes to <external files>/import/<title ID>/, and the launcher takes it at its start and whenever it comes back to the front, with the same dialogs as an
    // import from the picker. One at a time; a game that is running waits until it isn't
    static final String SEEN = "import_seen_";
    void incoming() {
        if (busy || source != null) return;
        File[] ds = new File(l.ext, "import").listFiles(); if (ds == null) return;
        java.util.Arrays.sort(ds);
        String running = l.runningGame();
        for (File d : ds) {
            if (!d.isDirectory() || !d.getName().matches("(?i)0[1-7][0-9a-f]{14}")) continue;
            if (l.app.getLong(SEEN + d.getName(), -1) == d.lastModified()) continue;
            final String id = d.getName().toUpperCase(Locale.ROOT);
            if (id.equalsIgnoreCase(running)) continue;
            Launcher.Game g = null; for (Launcher.Game x : l.scan()) if (x.id.equals(id)) g = x;
            if (g == null) continue;   // the game isn't on the phone (yet)
            Log.i(Launcher.TAG, "a save for " + id + " came from the computer: " + d);
            source = d; computer = true;
            choose(g, Saves.find(d, id, Saves.names(new File(saves(), id)), Saves.names(new File(saves(), id + "_device"))));
            return;
        }
    }

    // ---------------- earlier saves ----------------
    void restoreAsk(final Launcher.Game g) {
        final List<Saves.Found> ks = Saves.kept(backups(), g.id);
        if (ks.isEmpty()) { info(Loc.t("No earlier saves", "没有更早的存档"), Loc.f("No saves of %s are kept on this phone. An import keeps the save it replaces, and Back up saves on the games list keeps every game's.", "这台手机上没留着 %s 的存档。导入会保留被它替换的那份，「备份存档」会保留每个游戏的。", g.name)); return; }
        whenClosed(g, Loc.t("put a save back", "把存档放回去"), new Runnable() { public void run() {
            String[] items = new String[ks.size()];
            for (int i = 0; i < items.length; i++) items[i] = what(ks.get(i)) + "\n" + size(ks.get(i));
            new AlertDialog.Builder(l, DIALOG).setTitle(Loc.t("Put back which save?", "放回哪份存档？"))
                .setItems(items, new DialogInterface.OnClickListener() { public void onClick(DialogInterface d, int w) {
                    final Saves.Found f = ks.get(w);
                    new AlertDialog.Builder(l, DIALOG).setTitle(Loc.t("Put this save back?", "放回这份存档吗？"))
                        .setMessage(what(f) + "\n" + size(f) + Loc.t("\nIt holds: ", "\n内容：") + top(f.main(), 6) + "\n\n" + (hasSave(g.id) ? Loc.f("The save %s has now is kept first.", "%s 现在的存档会先保留。", g.name) : ""))
                        .setPositiveButton(Loc.t("Put it back", "放回去"), new DialogInterface.OnClickListener() { public void onClick(DialogInterface d2, int w2) { install(g, f, true); } })
                        .setNegativeButton(Loc.t("Cancel", "取消"), null).show();
                } }).setNegativeButton(Loc.t("Cancel", "取消"), null).show();
        } });
    }

    // ---------------- results from the pickers ----------------
    boolean result(int req, int res, Intent data) {
        if (req != EXPORT && req != IMPORT_FILE && req != IMPORT_FOLDER) return false;
        if (res != android.app.Activity.RESULT_OK || data == null || data.getData() == null) return true;
        Launcher.Game g = null; String id = l.app.getString(PREF, null);
        for (Launcher.Game x : l.scan()) if (x.id.equalsIgnoreCase(id)) g = x;
        if (g == null) { l.toast(Loc.f("The game %s is no longer on this phone", "这台手机上已经没有游戏 %s 了", id)); return true; }
        if (req == EXPORT) exportTo(g, data.getData()); else staged(g, data.getData(), req == IMPORT_FOLDER);
        return true;
    }

    // ---------------- words ----------------
    static String what(Saves.Found f) {
        String w;
        switch (f.format) {
            case "DroidPlay": w = Loc.t("A DroidPlay export or backup", "DroidPlay 导出的或备份的存档"); break;
            case "yuzu": w = Loc.f("A yuzu-family emulator's save (yuzu, Citron, Eden, Sudachi…), %s", "yuzu 系模拟器的存档（yuzu、Citron、Eden、Sudachi……），%s", word(f.label)); break;
            case "Ryujinx": w = Loc.f("A Ryujinx save folder, %s", "Ryujinx 的存档文件夹，%s", word(f.label)); break;
            case "JKSV": w = Loc.f("A JKSV backup, %s", "JKSV 的备份，%s", word(f.label)); break;
            case "EdiZon": w = Loc.f("An EdiZon backup, %s", "EdiZon 的备份，%s", word(f.label)); break;
            case "Checkpoint": w = Loc.f("A Checkpoint backup, %s", "Checkpoint 的备份，%s", word(f.label)); break;
            case "kept": w = f.label.matches("\\d{8}-\\d{6}-.+") ? when(f.label) + Loc.t(", kept when another save was put in", "，导入别的存档时留下的") : f.label.matches("\\d{8}-\\d{6}") ? when(f.label) + Loc.t(", from Back up saves", "，「备份存档」留下的") : f.label; break;
            case "title": w = Loc.t("A save folder named by its title ID", "以标题 ID 命名的存档文件夹"); break;
            default: w = f.label.isEmpty() ? Loc.t("A save, the zip's files", "一份存档，zip 里的文件") : Loc.f("A save folder, %s", "存档文件夹，%s", word(f.label));
        }
        return f.device != null && f.account == null && !f.format.equals("kept") ? w + Loc.t(" (device save)", "（设备存档）") : w;
    }
    // Saves.label 的英文（"device save" / "user <ID>"）在界面上的中文：Saves.java 本身与语言无关（它被 JVM 测试直接调用）
    static String word(String label) {
        if (label == null || label.isEmpty()) return label;
        if (label.equals("device save")) return Loc.t("device save", "设备存档");
        if (label.startsWith("user ")) return Loc.f("user %s", "用户 %s", label.substring(5));
        return label;
    }
    // Saves.top 的「还有 N 项」在界面上的中文
    static String top(File save, int max) {
        String t = Saves.top(save, max);
        java.util.regex.Matcher m = java.util.regex.Pattern.compile(" and (\\d+) more$").matcher(t);
        return m.find() ? t.substring(0, m.start()) + Loc.f(" and %d more", " 等 %d 项", Integer.parseInt(m.group(1))) : t;
    }
    static String size(Saves.Found f) {
        String bytes = f.bytes < (1 << 20) ? (f.bytes + 1023) / 1024 + " KB" : String.format(Locale.ROOT, "%.1f MB", f.bytes / 1048576.0);
        String count = Loc.zh() ? f.files + " 个文件，" + bytes : String.format(Locale.ROOT, "%d %s, %s", f.files, f.files == 1 ? "file" : "files", bytes);
        return count + (f.newest > 0 ? Loc.f(", last changed %s", "，最后修改 %s", DateFormat.getDateTimeInstance(DateFormat.MEDIUM, DateFormat.SHORT).format(new Date(f.newest))) : "");
    }
    static String when(String folder) {   // a backup folder's name, yyyyMMdd-HHmmss[-<title ID>], as a date
        try { return DateFormat.getDateTimeInstance(DateFormat.MEDIUM, DateFormat.SHORT).format(new SimpleDateFormat("yyyyMMdd-HHmmss", Locale.ROOT).parse(folder.substring(0, Math.min(15, folder.length())))); }
        catch (ParseException e) { return folder; }
    }
    static String now() { return new SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.ROOT).format(new Date()); }
    static String fileName(String s) { return s.replaceAll("[/\\\\:*?\"<>|]", "").trim(); }
    String name(Uri uri) {
        try (Cursor c = cr().query(uri, new String[] {OpenableColumns.DISPLAY_NAME}, null, null, null)) { if (c != null && c.moveToFirst()) return c.getString(0); }
        catch (Exception e) { /* a provider without names */ }
        return uri.getLastPathSegment();
    }
    // in → f, at most max bytes. → the bytes copied
    static long copy(InputStream in, File f, long max) throws IOException {
        long n = 0; byte[] b = new byte[1 << 16];
        f.getParentFile().mkdirs();
        try (OutputStream o = new FileOutputStream(f)) { for (int k; (k = in.read(b)) > 0; ) { if ((n += k) > max) throw new IOException("too big"); o.write(b, 0, k); } }
        return n;
    }

    // ---------------- the progress dialog ----------------
    void working(String what, final Runnable bg) {
        busy = true;
        progress = new AlertDialog.Builder(l, DIALOG).setMessage(what).setCancelable(false).show();
        new Thread(new Runnable() { public void run() {
            try { bg.run(); }
            catch (RuntimeException e) { Log.w(Launcher.TAG, "saves: " + e); done(Loc.t("Something went wrong", "出错了"), String.valueOf(e)); }   // the dialog never left up
        } }, "saves").start();
    }
    void say(final String s) { l.runOnUiThread(new Runnable() { public void run() { if (progress != null) progress.setMessage(s); } }); }
    void then(final Runnable r) {
        l.runOnUiThread(new Runnable() { public void run() {
            if (progress != null) { try { progress.dismiss(); } catch (Exception gone) { /* the window went with a recreated activity */ } progress = null; }
            busy = false; r.run();
        } });
    }
    void done(final String title, final String msg) { then(new Runnable() { public void run() { info(title, msg); } }); }
    void info(String title, String msg) { new AlertDialog.Builder(l, DIALOG).setTitle(title).setMessage(msg).setPositiveButton(Loc.t("OK", "确定"), null).show(); }
}
