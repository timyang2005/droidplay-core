// 界面文案的中英双语（汉化补丁）：系统的语言是中文时显示中文，是别的语言时显示英文原文。
//   这个 APK 没有 res/values 资源（aapt2 只链 apk/res 下的图标），界面的每一句都写在 dm/android/java 的这几个类里，
//   所以给每句一个（英文，中文）的写法：Loc.t("Play", "开始游戏") 在中文系统上取后者，Loc.f 是带参数的格式串。
//   不翻译的：游戏自己的名字和版本（control.nacp）、存档里的文件路径、按钮字母（A/B/X/Y/…）、logcat 的日志。
package org.nxnative.android;

import java.util.Locale;

final class Loc {
    private Loc() { }

    // 中文（简体、繁体、港澳）都按中文显示：语言码 zh（普通话）或 yue（粤语）
    static boolean zh() {
        String l = Locale.getDefault().getLanguage();
        return "zh".equals(l) || "yue".equals(l);
    }

    // 一句文案：en 是英文原文，zh 是中文译文
    static String t(String en, String zh) { return zh() ? zh : en; }

    // 带参数的文案：en、zh 都是 String.format 的格式串（两边的占位符个数要一样），args 依次填进去
    static String f(String en, String zh, Object... args) { return String.format(Locale.ROOT, zh() ? zh : en, args); }
}
