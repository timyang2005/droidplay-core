"""Plain words for what went wrong in DroidPlay for Windows (scripts/nxnative_android.py): explain() turns the packing script's and adb's own messages into a
title, what to do, and the one button that does it, for the Builds page's failure banner, the Library's statuses and the toasts. The raw message stays on screen
beside it. And the report a player copies for the Discord's #help (Markdown under its 2,000-character limit) or saves in full, with the home folder written as ~
and anything that looks like key material dropped, as scripts/bug_report.py does. Qt-free, so dm/tools/tests/test_android_desktop.py tests the rules against the
real messages without PySide6."""
import platform
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import i18n as L   # noqa: E402  # pyright: ignore[reportMissingImports]  (this folder's: Chinese on a Chinese system, English elsewhere; the tests read English)
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
import bug_report   # noqa: E402  # pyright: ignore[reportMissingImports]  (scripts/, put on the path above: its redaction)

DISCORD = 'https://discord.gg/3r92f8wmh7'
DISCORD_LIMIT = 2000   # characters in one message
ISSUE_441 = 'https://github.com/enjoyerofslop/droidplay-core/issues/441'   # games only a Mac build can capture run-time shaders for


@dataclass
class Help:
    title: str
    body: str          # rich text: names in it are escaped
    action: str = ''   # what its button does: phone, retry, keys, tools, folder, backup, issue (ISSUE_441); '' for none
    label: str = ''    # the button's text
    bug: bool = False  # nothing the player did or can fix: the report for #help is what to do


def esc(s): return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


# The script's stage names as a player reads them (its own name stays beside, in the report and the Builds page): a stage named with a version or a file
# ("extract v393216") is matched by its first word
STAGES = {'build nx_extract': L.t('Preparing the game reader', '准备游戏读取器'), 'extract': L.t('Reading the game files', '读取游戏文件'), 'unpack': L.t('Reading the game files', '读取游戏文件'), 'check': L.t('Reading the game files', '读取游戏文件'),
          'decompress NSZ': L.t('Unpacking compressed game files', '解压压缩过的游戏文件'), 'rewrite': L.t("Adapting the game's code for Android", "改写游戏的代码以适配安卓"), 'shader split': L.t("Finding the game's shaders", "找出游戏的着色器"),
          'shaders for Vulkan': L.t("Translating shaders for your phone's GPU", "把着色器翻译给你手机的 GPU"), 'Android host': L.t("Building the game's engine", "构建游戏的引擎"), 'APK': L.t('Packing the DroidPlay app', '打包 DroidPlay 应用'),
          'install and copy to the phone': L.t('Copying the game to the phone', '把游戏复制到手机'), 'install': L.t('Installing DroidPlay on the phone', '在手机上安装 DroidPlay'),
          'copy the shaders to the phone': L.t('Copying the shaders to the phone', '把着色器复制到手机'), 'game app': L.t("Packing the game's own app", "打包游戏自己的应用"), 'move the one-game install': L.t('Moving the old install', '迁移旧的安装'),
          'JDK 21': L.t('Downloading Java', '下载 Java'), '.NET SDK 10': L.t('Downloading .NET', '下载 .NET'), 'Android command-line tools': L.t('Downloading the Android tools', '下载 Android 工具'),
          'Android SDK packages': L.t('Installing the Android SDK', '安装 Android SDK')}


def stage_name(tech):
    if not tech: return ''
    if tech.startswith('survey'): return L.t('Studying the game (experimental build)', '分析这个游戏（实验性构建）')
    return STAGES.get(tech) or STAGES.get(tech.split()[0]) or tech


NETWORK = ('urlopen error', 'timed out', 'getaddrinfo failed', 'name or service not known', 'temporary failure in name resolution', 'connection reset',
           'connectionreseterror', 'remotedisconnected', 'connection aborted', 'incompleteread', 'errno 11001', 'winerror 10054', 'winerror 10060', 'http error 5')
PC_FULL = ('not enough space on the disk', 'errno 28', 'winerror 112', 'no space left on device')


def script_error(stdout, stderr):
    """What a failed run of the script said, as explain() reads it: the lines before its error, then its [RED] lines, the error last. --info and --check send
    their notes to stderr and the error, printed after, to stdout; the app read stderr alone whenever it held anything, so a folder with a file the scan skipped
    showed that note, or nothing, where the reason belonged (Skyward Sword HD on Windows, 2026-11-13)"""
    lines = [x for x in f'{(stderr or "").strip()}\n{(stdout or "").strip()}'.splitlines() if x.strip()]
    reds = [x for x in lines if x.lstrip().startswith('[RED]')]
    if not reds: return '\n'.join(lines[-8:]) or 'no output'
    return '\n'.join([x for x in lines if x not in reds][-6:] + reds)[-2000:]


# The scan's words for a file it passed over (build_ipa_from_nsp.py scan_nsps): the file, and why
SKIPPED = re.compile(r'skipping (.+?): (neither an NSP.*|its content meta could not be read.*|no base game, update or DLC content meta.*)$', re.M)


def skipped_files(t):   # → rich text naming up to three files the scan passed over, and why, or ''
    s = SKIPPED.findall(t)
    if not s: return ''
    shown = '; '.join(f'<b>{esc(f)}</b> ({esc(why[:120])})' for f, why in s[:3])
    more = L.t(f' and {len(s) - 3} more', f' 等另外 {len(s) - 3} 个') if len(s) > 3 else ''
    return L.t(f' It passed over {shown}', f' 它跳过了 {shown}') + more + L.t('.', '。')


def explain(text, phone='', game='', stage='', setup=False, folder='', wifi=False, read=False):
    """text: what failed said (its [RED] lines, the last line); phone, game: their names; stage: the script's name of the stage it stopped in; setup: it was
    --setup (Install tools); folder: the game's folder; wifi: the phone was connected over Wi-Fi (wireless debugging); read: the Library's read of a game
    folder (--info), not a build. → Help"""
    t = text or ''; low = t.lower(); wifi = wifi or 'wireless debugging is still on' in low   # the script's own words for a Wi-Fi phone that didn't come back
    ph, the_phone, g = esc(phone) if phone else L.t('Your phone', '你的手机'), esc(phone) if phone else L.t('your phone', '你的手机'), esc(game) if game else L.t('The game', '游戏')
    adb_said = re.search(r'\badb\b', low) is not None   # an adb command's failure: "No space left on device" is then the phone's, not this PC's
    if 'INSTALL_FAILED_USER_RESTRICTED' in t:
        return Help(L.t('Your Xiaomi phone blocked the install', '小米手机拦住了安装'), L.t('In Developer options, turn on <b>Install via USB</b> (it may ask you to sign in to your Xiaomi account), ' 'then Install again.', '在开发者选项里打开 <b>USB 安装</b>（可能会要你登录小米账号），' '然后再装一次。'), 'retry', L.t('Install again', '再装一次'))
    m = re.search(r"compiles (\d+) of its shaders while it runs, with its own shader compiler \(GLSLC\), and game profile \w+'s shader tables need them", t)
    if m:   # build_android_from_nsp.py run_time_stop: not a bug to report, and nothing the player can fix on this PC
        mac = 'Only a build for the Mac captures them' in t
        return Help(L.t('Build it for the Mac first', '先为 Mac 构建一次') if mac else L.t('This game builds on a Mac only for now', '这个游戏目前只能在 Mac 上构建'),
                    L.t(f'{g} compiles {m[1]} of its shaders while it runs, and only a build on a Mac can capture them so far. ', f'{g} 有 {m[1]} 个着色器是运行时才编译的，目前只有 Mac 上的构建能捕获它们。')
                    + (L.t('Build it for the Mac with DroidPlay for Mac, then build it for Android again: this build takes them from there.', '用 DroidPlay for Mac 先为 Mac 构建一次，然后再为安卓构建：这次的构建会从那里取它们。') if mac else
                       L.t('Its fix is followed in droidplay-core issue #441 on GitHub.', '修复进度跟在上游 droidplay-core 的 issue #441。')),
                    '' if mac else 'issue', '' if mac else L.t('Follow the fix on GitHub', '在 GitHub 上跟进修复'))
    if 'INSTALL_FAILED_UPDATE_INCOMPATIBLE' in t or 'signed with another key' in t:
        return Help(L.t('DroidPlay on this phone came from another computer', '手机上这个 DroidPlay 是别的电脑装的'), L.t('To update it from this PC, copy the signing key (<b>.android\\nxnative-debug.jks</b> in ' 'your user folder) from that computer to this one. Uninstalling DroidPlay from the phone instead deletes its saves.', '要从这台电脑更新它，请把那台电脑上的签名密钥（<b>.android\\\\nxnative-debug.jks</b>，在' '你的用户文件夹里）复制到这台电脑。从手机上卸载 DroidPlay 会把它的存档一起删掉。'), 'backup', L.t('Back up saves', '备份存档'))
    m = re.search(r'the phone has ([\d.]+ [KMG]?B) free: .+? needs ([\d.]+ [KMG]?B).*?Free up ([\d.]+ [KMG]?B)', t, re.S)
    if m: return Help(L.t(f'Not enough space on {the_phone}', f'{the_phone} 空间不够'), L.t(f'{g} needs {m[2]} and {the_phone} has {m[1]} free. Free up {m[3]} (videos, other games), then Install again.', f'{g} 需要 {m[2]}，而 {the_phone} 只有 {m[1]} 可用。腾出 {m[3]}（视频、别的游戏），然后再装一次。'),
                      'retry', L.t('Install again', '再装一次'))
    m = re.search(r'The phone has only ([\d.]+ [KMG]?B) free', t)
    if m or 'INSTALL_FAILED_INSUFFICIENT_STORAGE' in t or (adb_said and 'no space left on device' in low):
        return Help(L.t(f'Not enough space on {the_phone}', f'{the_phone} 空间不够'), (L.t(f'{ph} has only {m[1]} free. ', f'{ph} 只有 {m[1]} 可用。') if m else '') + L.t('Free up a few GB (videos, other games), then Install again: ' 'a copy cut short carries on from where it stopped.', '腾出几个 GB（视频、别的游戏），然后再装一次：' '中断的复制会从断点继续。'), 'retry', L.t('Install again', '再装一次'))
    if ('unauthorized' in low or 'authorizing' in low) and 'http error' not in low:   # adb's state, not a web server's 401
        if wifi: return Help(L.t(f"{ph} doesn't know this PC over Wi-Fi", f"{ph} 在 Wi-Fi 上不认识这台电脑"), L.t('Pair it again: on the phone, Wireless debugging › Pair device with pairing code, then ' '<b>Pair over Wi-Fi…</b> on the Phones page.', '再配对一次：在手机上 无线调试 › 使用配对码配对设备，然后' '在「手机」页点 <b>Wi-Fi 配对…</b>。'), 'phone', L.t('Set up my phone…', '设置我的手机…'))
        return Help(L.t(f"{ph} hasn't allowed this PC yet", f"{ph} 还没有允许这台电脑"), L.t('Unlock it and tap <b>Allow</b> on "Allow USB debugging?" (tick "Always allow from this computer"). ' 'No prompt? Unplug it and plug it back in.', '解锁它，在「允许 USB 调试？」上点 <b>允许</b>（勾上「一律允许这台电脑」）。' '没有弹窗？把线拔下来重新插上。'), 'phone', L.t('Set up my phone…', '设置我的手机…'))
    m = re.search(r'lost the phone (\d+) times', low)   # the script gave up on a connection that kept dropping (survives_drops)
    if m:
        return Help(L.t(f'The connection to {the_phone} keeps dropping', f'到 {the_phone} 的连接一直在断'), L.t(f'It dropped {m[1]} times in one install. ', f'一次安装里断了 {m[1]} 次。') +
                    (L.t('Move the phone closer to the router (5 GHz is faster), keep it awake and charging, or use a USB cable for this install, then Install again: ' 'the copy carries on from where it stopped.', '把手机靠近路由器（5 GHz 更快）、让它亮着并充电，或者这次用数据线安装，然后再装一次：' '复制会从断点继续。') if wifi or 'router' in low else
                     L.t('Try another cable or USB port (one on the computer itself, not a hub), then Install again: the copy carries on from where it stopped.', '换一根线或一个 USB 口（插电脑本体，不要扩展坞），然后再装一次：复制会从断点继续。')), 'retry', L.t('Install again', '再装一次'))
    if ('device offline' in low or '(offline)' in low or 'no devices/emulators found' in low or re.search(r"device '?\S*'? not found", low)
            or 'exit status 255' in low or 'error: closed' in low or 'did not come back within' in low):
        if wifi: return Help(L.t(f'{ph} dropped off Wi-Fi', f'{ph} 从 Wi-Fi 上掉线了'), L.t('Wake it, and check that it is on the same network as this PC and that Wireless debugging is still on ' '(its address changes when Wireless debugging restarts: DroidPlay finds it again). Then Install again: the copy carries on from where ' 'it stopped.', '唤醒它，确认它和这台电脑在同一个网络、无线调试还开着' '（无线调试重启后它的地址会变：DroidPlay 会重新找到它）。然后再装一次：复制会从' '断点继续。'), 'retry', L.t('Install again', '再装一次'))
        return Help(L.t(f'{ph} stopped answering', f'{ph} 不再应答'), L.t('Unplug it and plug it back in, then Install again: the copy carries on from where it stopped. A different cable or USB ' 'port helps if it keeps happening.', '把线拔下来重新插上，然后再装一次：复制会从断点继续。如果一直这样，换个' '线或 USB 口试试。'), 'retry', L.t('Install again', '再装一次'))
    if re.search(r'\b0 adb devices ready', low):
        return Help(L.t('No phone connected', '没有连接手机'), L.t('Plug in your phone with a USB cable that carries data, with USB debugging on, or connect it over Wi-Fi on the Phones page ' '(Android 11 and later).', '用能传数据的 USB 线把手机插上、打开 USB 调试，或者在「手机」页用 Wi-Fi 连上' '（安卓 11 及以后）。'), 'phone', L.t('Set up my phone…', '设置我的手机…'))
    m = re.search(r'less than ([\d.]+) GB free on the volume of (.+)', t)
    if m or any(x in low for x in PC_FULL):
        where = m[2].strip() if m else folder or ''
        d = re.match(r'[A-Za-z]:', where); drive = L.t(f' on drive {d[0].upper()}', f'（{d[0].upper()} 盘）') if d else ''   # a Windows path's, read on any system
        more = L.t(f'about {m[1]} GB free', f'约 {m[1]} GB 可用') if m else L.t('more room', '更多空间')
        return Help(L.t('Not enough space on this PC', '这台电脑空间不够'), L.t(f'Building {g.lower() if not game else g} needs {more}{drive}', f'构建 {g.lower() if not game else g} 需要{more}{drive}') + (L.t(f' (in {esc(where)})', f'（在 {esc(where)}）') if where else '') +
                    L.t(". Free some up, or move the game's folder to a drive with more room.", "。腾出一些空间，或者把游戏的文件夹移到空间更大的盘。"), 'folder' if where else '', L.t('Open the folder', '打开文件夹') if where else '')
    m = re.search(r'prod\.keys has no \S+ \(master key \w+, which came with ((?:firmware|a firmware after) [\w.]+)\)', t)
    if m: return Help(L.t('Your keys are older than this game', '你的密钥比这个游戏旧'), L.t(f'It needs keys from a Switch on {esc(m[1])}{"" if "after" in m[1] else " or later"}. Update your Switch, ' 'dump prod.keys again, and pick the new file.', f'它需要 {esc(m[1])}{"" if "after" in m[1] else " 或更新"} 的 Switch 上的密钥。更新你的 Switch，' '重新导出 prod.keys，再选新文件。'), 'keys', L.t('Choose prod.keys…', '选择 prod.keys…'))
    if 'no title key for rights id' in low or 'has no common ticket' in low:
        return Help(L.t("This game file can't be opened with your keys", "这个游戏文件用你的密钥打不开"), L.t('The file has no ticket for it. Dump the game again from your Switch, with its ticket.', '文件里没有它的票据。从你的 Switch 上重新导出这个游戏，带上它的票据。'))
    # a game that draws with OpenGL or Vulkan (build_android_from_nsp.py unsupported_graphics): nothing the player can change, and not a bug to report. It showed as "The build
    # stopped at Reading the game files" for Football Manager 2024 Touch (droidplay-core#476)
    m = re.search(r'(?:\[RED\] )?([^\n]*?) draws with (OpenGL|Vulkan), not NVN', t)
    if m:
        name = g if game else (esc(m[1]) or L.t('This game', '这个游戏'))
        return Help(L.t("This game isn't supported on Android yet", '这个游戏还不支持在安卓上跑'),
                    L.t(f"{name} draws with {m[2]}, and DroidPlay on Android runs only games that draw with NVN, the Switch's own "
                        'graphics API, so far: on the phone it would stop at its first graphics call, so it isn\'t built. Nothing on this PC or in the game files needs fixing.',
                        f'{name} 用的是 {m[2]}，而安卓上的 DroidPlay 目前只跑用 NVN（Switch 自己的图形接口）画图的游戏：'
                        '放到手机上它会在第一次图形调用时就停，所以这里不构建它。这台电脑和游戏文件都不需要改什么。'))
    # the game reader (nx_extract, built with .NET the first time a game is read) couldn't get its NuGet packages: NU1100 "Unable to resolve 'LibHac'" with
    # nuget.org missing or turned off in .NET's sources, NU1301 when the source can't be reached. It showed as "The build stopped" on a Windows PC (2026-11-13)
    if re.search(r'\bNU1(100|101|301)\b', t) or "unable to resolve 'libhac" in low or 'unable to load the service index' in low:
        return Help(L.t("DroidPlay couldn't download its game reader", 'DroidPlay 下载不了它的游戏读取器'),
                    L.t("The first time it reads a game, DroidPlay builds a small game reader with .NET, which "
                        "downloads its parts from nuget.org, and .NET couldn't get them. Check this PC is online. If it is, nuget.org may be missing or turned off in "
                        ".NET's settings: in a Command Prompt, <b>dotnet nuget list source</b> shows them; <b>dotnet nuget enable source nuget.org</b> turns it back "
                        "on, or <b>dotnet nuget add source https://api.nuget.org/v3/index.json -n nuget.org</b> adds it. Then open DroidPlay again.",
                        '第一次读游戏时，DroidPlay 会用 .NET 构建一个小游戏读取器，它要从 nuget.org 下载需要的组件，而 .NET 拿不到。先确认这台电脑能上网。'
                        '能上网的话，可能是 nuget.org 在 .NET 的设置里缺失或被关掉了：在命令提示符里，<b>dotnet nuget list source</b> 会列出它们；'
                        '<b>dotnet nuget enable source nuget.org</b> 把它重新打开，或者 <b>dotnet nuget add source https://api.nuget.org/v3/index.json -n nuget.org</b> 把它加上。'
                        '然后重新打开 DroidPlay。'))
    # what reading the folder found (build_ipa_from_nsp.py scan_nsps), before anything is built: said as what to change in the folder, which the button opens
    show = ('folder', L.t('Open the folder', '打开文件夹')) if folder else ('', '')
    m = re.search(r'more than one game in the folder: ([^;]+);', t)
    if m:
        return Help(L.t('More than one game in this folder', '这个文件夹里有不止一个游戏'),
                    L.t(f'DroidPlay reads one game per folder: the game with its own updates and DLC. This folder holds the games {esc(m[1])}. Move each game into a folder of its own, then add those folders.',
                        f'DroidPlay 一个文件夹只读一个游戏：游戏本体连同它自己的更新和 DLC。这个文件夹里有这些游戏：{esc(m[1])}。请把每个游戏分别放进自己的文件夹，再添加那些文件夹。'), *show)
    if 'no base game nsp found' in low:
        return Help(L.t('The game itself is missing from this folder', '这个文件夹里缺游戏本体'),
                    L.t("This folder has the game's update or DLC but not the game: put the base game's XCI (the "
                        'cartridge) or NSP in the same folder, beside the update.',
                        '这个文件夹里有游戏的更新或 DLC，但没有游戏本体：请把本体的 XCI（卡带导出的）或 NSP 放进同一个文件夹，和更新放在一起。'), *show)
    m = re.search(r'no NSP for update (\S+) \(the game profile needs these versions: ([^)]+)\)', t)
    if m:
        return Help(L.t('An update the build needs is missing', '构建需要的更新缺失'),
                    L.t(f"{g} is built from versions {esc(m[2])}, and this folder has no NSP for update {esc(m[1])}. Put "
                        "that update's NSP in the game's folder, beside the base game.",
                        f'{g} 要按版本 {esc(m[2])} 构建，而这个文件夹里没有更新 {esc(m[1])} 的 NSP。请把那个更新的 NSP 放进游戏的文件夹，和本体放在一起。'), *show)
    if 'no game package with a readable content meta' in low:
        return Help(L.t('No game DroidPlay can open in this folder', '这个文件夹里没有 DroidPlay 能打开的游戏'),
                    L.t("DroidPlay needs the game's own .nsp or .xci files: not a .zip or .rar, not a dump split into "
                        'parts (join them into one file first), and fully on this PC (OneDrive\'s online-only files can\'t be read). If the files are right, pick '
                        'your prod.keys again: keys from another Switch can\'t open them.',
                        'DroidPlay 需要游戏自己的 .nsp 或 .xci 文件：不是 .zip 或 .rar，不是被拆成几段导出的（请先合并成一个文件），'
                        '而且要完整地在这台电脑上（OneDrive 的「仅在线」文件读不了）。如果文件没问题，请重新选一次 prod.keys：别的 Switch 上的密钥打不开它们。')
                    + skipped_files(t), *show)
    if 'give -k' in low or ('prod.keys' in low and 'needs' in low and 'keys' in low and 'master key' not in low):
        return Help(L.t('DroidPlay needs your keys', 'DroidPlay 需要你的密钥'), L.t('NSP and XCI games are encrypted: pick your prod.keys first.', 'NSP 和 XCI 游戏是加密的：先选你的 prod.keys。'), 'keys', L.t('Choose prod.keys…', '选择 prod.keys…'))
    if 'needs dotnet' in low or 'install the .net 10 sdk' in low:
        return Help(L.t('Install the tools first', '先装工具'), L.t("DroidPlay reads and builds games with tools it hasn't installed yet.", "DroidPlay 读游戏、构建游戏要用的工具还没装。"), 'tools', L.t('Install tools…', '安装工具…'))
    if 'does not match its' in low:
        return Help(L.t('The download came through damaged', '下载内容损坏了'), L.t("It didn't match what its publisher lists, so DroidPlay deleted it. Try again; if it keeps happening, something " 'on your network is changing downloads.', "它和发布方给出的校验值不一致，DroidPlay 已经删掉了。再试一次；如果一直这样，说明" '你的网络上有东西在改下载内容。'), 'retry', L.t('Try again', '再试一次'))
    if any(x in low for x in NETWORK):
        return Help(L.t('The download stopped', '下载中断了'), L.t(f'Check your internet connection, then {"Install tools" if setup else "try"} again.', f'检查网络连接，然后再{"安装工具" if setup else "试"}一次。'), 'retry', L.t('Try again', '再试一次'))
    if read:   # the Library's read of a folder, not a build: no report to copy there, so the message itself (shown under it) is what to post
        return Help(L.t("DroidPlay couldn't read this game", 'DroidPlay 读不了这个游戏'),
                    L.t('This is probably a bug in DroidPlay, not something you did. Post what it said (below) in <b>#help</b> '
                        'on the Discord.',
                        '这多半是 DroidPlay 的 bug，不是你操作的问题。把它底下说的话发到 Discord 的 <b>#help</b>。'), *show, bug=True)
    what, at = L.t('Installing the tools', '正在安装工具') if setup else L.t('The build', '构建'), stage_name(stage)
    return Help(L.t(f'{what} stopped at "{at}"', f'{what}停在「{at}」') if at else L.t(f'{what} stopped', f'{what}停了'), L.t('This is probably a bug in DroidPlay, not something you did. Copy the report and post it in ' '<b>#help</b> on the Discord.', '这多半是 DroidPlay 的 bug，不是你操作的问题。复制报告，发到 ' 'Discord 的 <b>#help</b>。'), bug=True)


# Games that compile some of their shaders while they run, with their own GLSLC (build_android_from_nsp.py run_time_missing, run_time_note): the Library's words before a build,
# and the Builds page's after one says so (its run_time_shaders event)
RUN_TIME_META = L.t('compiles some shaders while it runs: after its first scene, Manage › Update shaders from the phone',
                    '有一部分着色器在运行时才编译：玩到第一幕后，用 管理 › 从手机更新着色器')


def mac_only(count, mac=False):   # the status of a game whose profile's tables need shaders it compiles while it runs, with no Mac build's captures on this computer (#441)
    return (L.t(f'Build it for the Mac first: it compiles {count} shaders while it runs', f'先为 Mac 构建一次：它有 {count} 个着色器是运行时才编译的') if mac else
            L.t(f'Builds on a Mac only for now: it compiles {count} shaders while it runs', f'目前只能在 Mac 上构建：它有 {count} 个着色器是运行时才编译的'))


def run_time_note(game='', game_app=False):   # → (title, body) of the Builds page's notice for a provisional profile's game that compiles shaders while it runs
    g = esc(game) if game else L.t('The game', '游戏')
    if game_app: return (L.t('Some shaders come later', '有些着色器要晚一点才有'),
                         L.t(f'{g} compiles some of its shaders while it runs, so this game app may draw some things black, and it can\'t take them in '
                             'later. To pack them, install the game with DroidPlay first, play it to its first scene, use Manage › Update shaders from the phone, then build the '
                             'game app again.',
                             f'{g} 有一部分着色器是在运行时才编译的，所以这个游戏应用可能会把一些东西画成黑的，而且之后补不进去。要把它们打包进去：'
                             '先用 DroidPlay 安装这个游戏，玩到第一幕，用 管理 › 从手机更新着色器，然后再构建一次游戏应用。'))
    return (L.t('Some shaders come after the first play', '有些着色器要等第一次玩过才有'),
            L.t(f'{g} compiles some of its shaders while it runs, so the first install may draw some things black. Play it to its '
                'first scene, then use Manage › Update shaders from the phone to bring them in.',
                f'{g} 有一部分着色器是在运行时才编译的，所以第一次安装后可能会把一些东西画成黑的。玩到第一幕，然后用 管理 › 从手机更新着色器 把它们取进来。'))


# ---- the report ----
def system_name():
    if sys.platform == 'win32':
        b = sys.getwindowsversion().build   # pyright: ignore[reportAttributeAccessIssue]  (Windows only)
        return f'Windows {11 if b >= 22000 else 10} (build {b})'
    return f'{platform.system()} {platform.release()}'


def redact(text, home):   # bug_report's rules; Windows spells the home folder with \ and, in some tools' messages, with /. And the phone's serial, which a post
    # in a public channel has no need of: the script's --serial and adb's -s name it
    if home: text = text.replace(home.replace('\\', '/'), home)
    text = re.sub(r'(--serial[ =]|--phone-id[ =]|\badb(?:\.exe)? -s )\S+', r'\1<serial>', text)
    text = re.sub(r'\badb-[A-Za-z0-9]+-[^\s.]+\._adb-tls-(?:connect|pairing)\._tcp\.?', '<serial>', text)   # a Wi-Fi phone's mDNS name carries its serial number
    return bug_report.redact(text, home)[0]


def header(info):   # info: version, title, stage, k, n, game, game_id, game_version, phone, android, gpu
    st = info.get('stage') or ''
    lines = [f'**DroidPlay {info.get("version") or "?"}** on {system_name()}',
             f'**{info.get("title") or "A build"}** stopped' + (f' at {stage_name(st)} (`{st}`' + (f', stage {info["k"]} of {info["n"]}' if info.get('k') else '') + ')' if st else '')]
    if info.get('game_id'): lines.append(f'Game: {info.get("game") or "?"} `{info["game_id"]}`' + (f' v{info["game_version"]}' if info.get('game_version') else ''))
    if info.get('phone'):
        lines.append('Phone: ' + ' · '.join(x for x in (info['phone'], f'Android {info["android"]}' if info.get('android') else '', info.get('gpu') or '') if x))
    return lines


def markdown_report(info, reds, log_lines, home, limit=DISCORD_LIMIT - 10):
    """The report to paste in #help: who, what, where it stopped, its [RED] lines and the last lines of its log, cut to fit one Discord message"""
    reds = list(dict.fromkeys(r.strip() for r in reds if r.strip()))[-6:]; tail = [x for x in log_lines if x.strip()][-15:]
    def make(reds, tail):
        out = header(info)
        if reds: out += ['**Error**', '```text', *reds, '```']
        if tail: out += ['**Last lines**', '```text', *tail, '```']
        return redact('\n'.join(out), home)
    text = make(reds, tail)
    while len(text) > limit and tail: tail = tail[1:]; text = make(reds, tail)
    while len(text) > limit and len(reds) > 1: reds = reds[1:]; text = make(reds, tail)
    if len(text) > limit: text = make([r[-300:] for r in reds], tail)
    return text[:limit]


def full_report(info, log_text, journal, home):   # Save full report: the same header, where the journal is, and the whole log
    head = [x.replace('**', '').replace('`', '') for x in header(info)]
    return redact('\n'.join(head + ['', f'Journal: {journal}' if journal else 'Journal: none', '', '---- log ----', log_text]), home)
