"""Where a game's data goes on the phone, in DroidPlay for Windows (scripts/nxnative_android.py): the per-game choice Phone storage / SD card, which flags of
scripts/build_android_from_nsp.py it becomes for each kind of run, and the words that say what it means. Qt-free, so dm/tools/tests/test_android_desktop.py
tests the rules without PySide6. The card itself is found by the script's own sd_card_ids (sm list-volumes, else /storage); the app only runs the two adb calls."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import i18n as L   # noqa: E402  # pyright: ignore[reportMissingImports]  (this folder's: Chinese on a Chinese system, English elsewhere; the tests read English)

PHONE, SD = 'phone', 'sd'   # what is saved per game, under data/<title ID>

LABELS = {PHONE: L.t('Phone storage', '手机存储'), SD: L.t('SD card', 'SD 卡')}

# Why the choice says all of this: the data is gigabytes, the player gives up a card's copy by hand, and a game whose data is on a card that is out does not start
MEANING = (L.t('Game data: on the SD card, the game\'s data (gigabytes) goes in DroidPlay\'s own folder there and the rest of the game stays on the phone. ' 'The game won\'t start without the card in the phone. Going back to Phone storage copies the data back to the phone and leaves the card\'s copy for you to delete.', '游戏数据：放在 SD 卡上时，游戏的数据（几个 GB）放进 DroidPlay 在卡上自己的文件夹，游戏其余部分留在手机上。' '手机里没有这张卡，游戏就启动不了。改回手机存储会把数据复制回手机，卡上那份留给你自己删。'))
MEANING_APP = (L.t('On the SD card, the data stays out of the APK, in a .romfs file beside it that you copy to the card and pick when the app first opens. ' 'The app won\'t start without the card.', '放在 SD 卡上时，数据不进 APK，而是放在它旁边的一个 .romfs 文件里，你把它复制到卡上，第一次打开应用时选它。' '没有这张卡，应用就启动不了。'))


def valid(choice): return choice if choice in (PHONE, SD) else PHONE   # anything else saved, or nothing, is the default


def offered(cards):   # SD card is offered when the phone has exactly one: two cards would make the script ask which, so that goes by --romfs-dir on the command line
    return len(cards) == 1


def no_card_note(cards):   # why the choice is not offered, '' when it is
    if offered(cards): return ''
    if not cards: return L.t('The picked phone has no SD card, or none is connected, so the game data goes on the phone.', '选中的手机没有 SD 卡，或者没插卡，所以游戏数据放在手机上。')
    return f'The picked phone has {len(cards)} SD cards. DroidPlay puts the data on one card only; on the command line, --romfs-dir takes the folder of the one you want.'


def flags(choice, extra):   # the script's flags for the saved choice, given the run's own (--push-only, --game-apk, ...): only a run that copies the game to a phone, or a game app's APK, takes one
    if valid(choice) != SD: return []
    if '--game-apk' in extra: return [] if '--xapk' in extra else ['--romfs-beside']   # an XAPK carries the data as its OBB file
    if any(x in extra for x in ('--no-push', '--update-shaders', '--apk-only', '--migrate')): return []
    return ['--romfs-dir', 'sd']


def problem(choice, extra, cards):   # a run that can't take the saved choice, in words, before the script stops on it: '' when it can
    if flags(choice, extra) != ['--romfs-dir', 'sd']: return ''
    if not offered(cards): return L.t('This game\'s data is set to the SD card (Options), and ', '这个游戏的数据设成了 SD 卡（选项），而') + (
        L.t('the phone has no SD card in it.', '手机里没有插 SD 卡。') if not cards else L.t(f'the phone has {len(cards)} SD cards.', f'手机里插着 {len(cards)} 张 SD 卡。')) + L.t(' Put the card in, or pick Phone storage.', ' 插上卡，或者改成手机存储。')
    return ''
