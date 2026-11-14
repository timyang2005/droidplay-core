// The Remove game row of a game's settings screen (Launcher.java), and the same from a game the installed app has no host for: deletes the game's files from the phone
// after saying what goes and how much space it frees, and keeps its save. Removal.java finds and deletes the files; this file is the row and the dialogs, with
// LauncherSaves' row, progress dialog and busy flag, so a removal and a save's copy never run at once (nor Play during either). Never while the game runs: its host
// reads those files and writes its pipeline cache back, so the player is asked to close it first, and the game is looked for again just before anything goes.
//   A game app (a game packed as an app of its own, GameStart.java) has no folder in this app: it is removed as any app is, by uninstalling it (docs/android.md).
package org.nxnative.android;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.util.Log;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;

import java.io.File;

final class LauncherRemove {
    final Launcher l;
    LauncherRemove(Launcher l) { this.l = l; }
    LauncherSaves s() { return l.saves; }

    View rows(final Launcher.Game g) {
        LinearLayout box = new LinearLayout(l); box.setOrientation(LinearLayout.VERTICAL);
        TextView h = l.caps(Loc.t("Remove", "移除")); h.setPadding(0, l.px(18), 0, l.px(6)); box.addView(h);
        box.addView(s().row(Loc.t("Remove game", "移除游戏"),
            Loc.t("Deletes the game from this phone to free its space. Its save stays, for when you install it again.",
                  "把游戏从这台手机上删掉，腾出它占的空间。存档会留着，等你以后再装回来。"),
            Loc.t("Remove…", "移除…"),
            new Runnable() { public void run() { ask(g); } }));
        return box;
    }

    // The game closed first when it runs (after asking), then its files added up off the UI thread (a game's shaders are tens of thousands of files), then the prompt
    void ask(final Launcher.Game g) {
        if (s().busy) return;
        s().whenClosed(g, Loc.t("remove it", "移除它"), new Runnable() { public void run() {
            s().working(Loc.f("Adding up what %s takes…", "正在统计 %s 占多大…", g.name), new Runnable() { public void run() {
                final Removal r = new Removal(g.dir, l.internal, g.id);
                s().then(new Runnable() { public void run() { confirm(g, r); } });
            } });
        } });
    }

    // Where the image in a folder of its own is, in the player's words: Removal.where() stays English, as dm/tools/tests/test_android_remove.py reads it
    static String placeZh(File romfs) {
        String en = Removal.where(romfs);
        return en.equals("on the SD card") ? "SD 卡上" : en.startsWith("in ") ? en.substring(3) + " 里" : en;
    }

    void confirm(final Launcher.Game g, final Removal r) {
        final boolean saved = s().hasSave(g.id);
        StringBuilder m = new StringBuilder(Loc.f("%s's code, shaders and game data are deleted from this phone, freeing %s.",
                                                 "%s 的代码、着色器和游戏数据会从这台手机上删掉，腾出 %s。", g.name, Removal.size(r.bytes())));
        if (r.romfs != null && r.romfsThere) m.append(Loc.f(" That includes its game data %s.", " 其中也包括它放在%s的游戏数据。",
                                                            Loc.t(Removal.where(r.romfs), placeZh(r.romfs))));
        else if (r.romfs != null) m.append(Loc.f("\n\nIts game data was copied to %s, which can't be seen now (the SD card taken out?), so it stays there: delete it yourself.",
                                                 "\n\n它的游戏数据复制到了 %s，现在看不到（SD 卡是不是拔掉了？），所以留在了那里：请自己删掉。", r.romfs.getParent()));
        m.append("\n\n").append(saved ? Loc.t("Its save stays on this phone, and is there again when you install the game again.",
                                              "存档会留在这台手机上，等你再装这个游戏时它还在。")
                                     : Loc.t("It has no save on this phone to keep.", "这台手机上没有它的存档可留。"));
        m.append("\n\n").append(Loc.t("This can't be undone: to play it again, install it again from your computer.",
                                      "删掉就恢复不了：想再玩，得从电脑上重新安装。"));
        AlertDialog.Builder b = new AlertDialog.Builder(l, LauncherSaves.DIALOG).setTitle(Loc.f("Remove %s?", "移除 %s？", g.name)).setMessage(m)
            .setPositiveButton(Loc.t("Remove", "移除"), new DialogInterface.OnClickListener() { public void onClick(DialogInterface d, int w) { remove(g, r, saved); } })
            .setNegativeButton(Loc.t("Cancel", "取消"), null);
        if (saved) b.setNeutralButton(Loc.t("Export save first", "先导出存档"), new DialogInterface.OnClickListener() { public void onClick(DialogInterface d, int w) { s().export(g); } });
        b.show();
    }

    void remove(final Launcher.Game g, final Removal r, final boolean saved) {
        String running = l.runningGame();
        if (running != null && running.equalsIgnoreCase(g.id)) { s().info(Loc.t("Nothing removed", "什么都没删"), Loc.f("%s is running: close it, then try again.", "%s 正在运行：关掉它，再试一次。", g.name)); return; }   // started from the computer meanwhile
        s().working(Loc.f("Removing %s…", "正在移除 %s…", g.name), new Runnable() { public void run() {
            final Removal.Tally t = r.remove();
            Log.i(Launcher.TAG, "launcher: removed " + g.id + " (" + g.dir + (r.romfs != null ? ", " + r.romfs : "") + ", cache/" + r.id + "): " + t.freed + " bytes freed"
                + (t.left > 0 ? ", " + t.left + " files or folders left, first " + t.leftAt : "") + "; the save stays");
            s().then(new Runnable() { public void run() {
                l.showGames();
                if (t.left == 0) l.toast(Loc.f("%s removed: %s freed.", "%s 已移除：腾出 %s。", g.name, Removal.size(t.freed))
                    + (saved ? Loc.t(" Its save stays.", " 存档保留。") : ""));
                else s().info(Loc.t("Some files stayed", "有些文件没能删掉"),
                    Loc.f("%s is off the games list and %s is freed, but some of its files couldn't be deleted, such as %s. Delete them from a computer with adb shell rm -r.",
                          "%s 已经不在游戏列表里了，也腾出了 %s，但它有些文件删不掉，比如 %s。请用电脑上的 adb shell rm -r 删掉。",
                          g.name, Removal.size(t.freed), t.leftAt));
            } });
        } });
    }
}
