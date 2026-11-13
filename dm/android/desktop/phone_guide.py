"""How to connect a phone, by brand, for DroidPlay for Windows' PhoneGuide dialog (scripts/nxnative_android.py): the steps that turn on USB debugging, each
maker's catch (Samsung's Auto Blocker greys the switch out, Xiaomi needs Install via USB, a Pixel may need Google's driver), and what to try when the phone
doesn't show up. And a phone's battery and free space from one adb shell call, with the warning a nearly flat phone needs: a PC's USB port charges slowly
(a Galaxy S25 Edge sat at 3-4% on the test PC) and an install runs for minutes. Qt-free, so dm/tools/tests/test_android_desktop.py tests it."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import i18n as L   # noqa: E402  # pyright: ignore[reportMissingImports]  (this folder's: Chinese on a Chinese system, English elsewhere; the tests read English)

INTRO = L.t("DroidPlay installs games over USB with Android's developer tools. You turn them on once, on the phone. Names vary a little between Android versions.",
            'DroidPlay 用安卓的开发者工具通过 USB 安装游戏。这些工具在手机上开一次就行。不同安卓版本里的叫法略有不同。')
PLUG = L.t('Plug the phone into this PC, unlock it, tick "Always allow from this computer" and tap <b>Allow</b>.', '把手机插到这台电脑上，解锁，勾上「一律允许这台电脑」，再点 <b>允许</b>。')
BUILD_NUMBER = L.t('tap <b>Build number</b> 7 times (enter your PIN if it asks): "You are now a developer".', '连点 <b>版本号</b> 7 次（要 PIN 就输）：提示「您现在已经是一名开发者」。')
GOOGLE_DRIVER = 'https://developer.android.com/studio/run/win-usb'

# (key, name, steps, a note under them)
BRANDS = (
    ('samsung', 'Samsung Galaxy', [
        f'Settings › About phone › Software information: {BUILD_NUMBER}',
        L.t('Settings › Security and privacy › <b>Auto Blocker</b>: turn it off. It blocks USB debugging and greys out the switch below. You can turn it back on ' 'when you\'re done installing games.', '设置 › 安全与隐私 › <b>自动拦截器（Auto Blocker）</b>：关掉它。它会拦住 USB 调试，并把下面的开关变灰。装完游戏以后可以再打开' '。'),
        L.t('Settings › <b>Developer options</b> (at the bottom of Settings): turn on <b>USB debugging</b>.', '设置 › <b>开发者选项</b>（在设置最下面）：打开 <b>USB 调试</b>。'),
        PLUG], L.t('No driver needed on Windows 10 or 11 (checked on a Galaxy S25 Edge).', 'Windows 10/11 上不需要驱动（在 Galaxy S25 Edge 上验过）。')),
    ('pixel', 'Google Pixel', [
        f'Settings › About phone: {BUILD_NUMBER}',
        L.t('Settings › System › Developer options: turn on <b>USB debugging</b>.', '设置 › 系统 › 开发者选项：打开 <b>USB 调试</b>。'),
        PLUG], f'If DroidPlay still doesn\'t see it, Windows may need <a href="{GOOGLE_DRIVER}">Google\'s USB driver</a>.'),
    ('xiaomi', 'Xiaomi, Redmi, POCO', [
        L.t('Settings › About phone: tap <b>OS version</b> (HyperOS) or <b>MIUI version</b> 7 times.', '设置 › 我的设备（关于手机）：连点 <b>OS 版本</b>（HyperOS）或 <b>MIUI 版本</b> 7 次。'),
        L.t('Settings › Additional settings › Developer options: turn on <b>USB debugging</b>, then <b>Install via USB</b> (Xiaomi asks you to sign in to a Xiaomi ' 'account, and may need a SIM card in the phone), then <b>USB debugging (Security settings)</b>.', '设置 › 更多设置 › 开发者选项：打开 <b>USB 调试</b>，再打开 <b>USB 安装</b>（小米会要你登录小米账号，手机里可能还得插着 SIM 卡），然后打开 <b>USB 调试（安全设置）</b>' '。'),
        PLUG], L.t('When DroidPlay installs, the phone may ask whether to allow it: tap <b>Install</b>.', 'DroidPlay 安装时手机可能会问要不要允许：点 <b>安装</b>。')),
    ('oneplus', 'OnePlus, OPPO, realme', [
        f'Settings › About device › Version: {BUILD_NUMBER}',
        L.t('Settings › System › Developer options (Additional settings on some): turn on <b>USB debugging</b>.', '设置 › 系统 › 开发者选项（有些机型在更多设置里）：打开 <b>USB 调试</b>。'),
        PLUG], ''),
    ('handheld', 'AYN, Retroid, AYANEO and other handhelds', [
        f'Settings › About (device or tablet): {BUILD_NUMBER}',
        L.t('Settings › System › Developer options: turn on <b>USB debugging</b>.', '设置 › 系统 › 开发者选项：打开 <b>USB 调试</b>。'),
        PLUG], ''),
    ('other', L.t('Other Android', '其他安卓'), [
        f'Settings › About phone: {BUILD_NUMBER}',
        L.t('Settings › Developer options (often under System): turn on <b>USB debugging</b>.', '设置 › 开发者选项（一般在系统下面）：打开 <b>USB 调试</b>。'),
        PLUG], ''),
)

TROUBLE = (
    (L.t("It charges but DroidPlay doesn't see it", "能充电，但 DroidPlay 看不到它"), L.t('Many cables that come with controllers and power banks only charge. Try the phone\'s own cable, in a port on the PC ' 'rather than a hub.', '很多手柄、充电宝配的线只能充电。换手机自己的线，插在电脑本体的接口上' '，不要插扩展坞。')),
    (L.t('"Allow USB debugging?" never appears', '一直不出现「允许 USB 调试？」'), L.t('Unlock the phone and pull down the notifications. Or, in Developer options, tap <b>Revoke USB debugging ' 'authorizations</b>, then unplug it and plug it back in.', '解锁手机，下拉通知栏。或者在开发者选项里点 <b>撤销 USB 调试授权</b>' '，再把线拔下来重新插上。')),
    (L.t('USB debugging is greyed out (Samsung)', 'USB 调试是灰的（三星）'), L.t('Turn off <b>Auto Blocker</b> (step 2).', '关掉 <b>自动拦截器</b>（第 2 步）。')),
    (L.t('Device Manager shows "ADB Interface" with a yellow mark', '设备管理器里「ADB Interface」带黄色感叹号'), L.t(f'Windows needs the maker\'s USB driver, or <a href="{GOOGLE_DRIVER}">Google\'s</a> for a Pixel.', f'Windows 需要厂商的 USB 驱动；Pixel 用 <a href="{GOOGLE_DRIVER}">Google 的</a>。')),
    (L.t('No cable?', '没有数据线？'), L.t('Android 11 and later can connect over Wi-Fi: Developer options › <b>Wireless debugging</b>, then <b>Pair over Wi-Fi…</b> on the Phones page.', '安卓 11 及以后可以用 Wi-Fi 连：开发者选项 › <b>无线调试</b>，再在「手机」页点 <b>Wi-Fi 配对…</b>。')),
)

# what adb's getprop ro.product.manufacturer says (a phone that hasn't allowed this PC yet gives only devices -l's model): a maker's name, or a handheld's
# board maker (a Retroid Pocket 5 says Moorechip)
MAKERS = (('samsung', ('samsung',)), ('pixel', ('google', 'pixel')), ('xiaomi', ('xiaomi', 'redmi', 'poco')), ('oneplus', ('oneplus', 'oppo', 'realme')),
          ('handheld', ('ayn', 'retroid', 'moorechip', 'ayaneo', 'anbernic')))


def brand_for(manufacturer='', model=''):
    words = f'{manufacturer} {model}'.lower()
    if re.match(r'\s*sm[-_ ]', model.lower()): return 'samsung'   # a Galaxy's model code (SM-S937U1), all a phone waiting for Allow shows
    return next((key for key, names in MAKERS if any(re.search(rf'\b{n}', words) for n in names)), 'other')


LOW_BATTERY = 20   # percent


def parse_status(text):
    """dumpsys battery's powered/level/status lines and df -k's last line, as one adb shell call prints them → {battery, charging, free} (absent when not printed)"""
    out = {}
    m = re.search(r'^\s*level:\s*(\d+)', text, re.M)
    if m: out['battery'] = int(m[1])
    m = re.search(r'^\s*status:\s*(\d+)', text, re.M)
    # BatteryManager's 2 charging, 5 full: a phone on a PC's USB port may show "USB powered: true" and still be discharging (4), as a OnePlus Pad 3 did
    if m: out['charging'] = m[1] in ('2', '5')
    row = next((l.split() for l in text.splitlines() if l.startswith('/') and len(l.split()) >= 6), None)
    if row and row[3].isdigit(): out['free'] = int(row[3]) * 1024
    return out


def size_text(n): return f'{n / 1e9:.0f} GB' if n >= 10e9 else f'{n / 1e9:.1f} GB' if n >= 1e9 else f'{n / 1e6:.0f} MB'


def battery_warning(d):
    b = d.get('battery')
    if b is None or b >= LOW_BATTERY: return ''
    return (L.t(f'Battery {b}%: a PC\'s USB port charges slowly, and an install takes a few minutes. Charge the phone a little first, from a wall charger.', f'电量 {b}%：电脑的 USB 口充得慢，而安装要几分钟。先用充电器给手机充一会儿。')
            if not d.get('charging') or b < 10 else L.t(f'Battery {b}%: it\'s charging, but slowly from a PC\'s USB port. An install takes a few minutes.', f'电量 {b}%：在充电，但电脑的 USB 口充得慢。安装要几分钟。'))


def readout(d):   # " · 212 GB free · battery 64%", for the phone's line on the checklist and the Phones page
    bits = ([L.t(f'{size_text(d["free"])} free', f'剩 {size_text(d["free"])}')] if d.get('free') is not None else []) + ([L.t(f'battery {d["battery"]}%', f'电量 {d["battery"]}%')] if d.get('battery') is not None else [])
    return ''.join(f' · {b}' for b in bits)
