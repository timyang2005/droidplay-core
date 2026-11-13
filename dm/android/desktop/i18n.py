"""文案的中英双语：系统的语言是中文时显示中文，其他语言显示英文原文。

和安卓端 Loc.java 是一套写法：t(英文, 中文)、f(英文, 中文, ...)。英文原文留在调用点，上游改了合并进来容易对上。
默认英文：单测（dm/tools/tests）和命令行工具的日志断言英文，所以只有桌面端窗口启动时才按系统的语言打开中文；
构建、--check 那些子进程由窗口传 DM_UI_LANG 环境变量，它们的进度和日志才跟着一起说中文。
"""
import os

_zh = None


def set_language(lang):
    """'zh-Hans'、'zh'、'yue' 是中文，别的都是英文。窗口启动时按 QLocale 调它。"""
    global _zh
    lang = (lang or '').lower()
    _zh = lang.startswith('zh') or lang.startswith('yue')


def set_zh(on):
    global _zh
    _zh = bool(on)


def zh():
    global _zh
    if _zh is None:
        env = os.environ.get('DM_UI_LANG', '').lower()
        _zh = env.startswith('zh') or env.startswith('yue')   # the window sets it (and hands it to the builds it starts); the tests and the console tools say nothing, and read English
    return _zh


def t(en, zh_text):
    return zh_text if zh() else en


def f(en, zh_text, *args):
    """两边都是格式串：中文那边的占位符按调用方的顺序给。"""
    return (zh_text if zh() else en) % args if args else (zh_text if zh() else en)
