"""
SendKeys.py - Sends one or more keystroke or keystroke combinations
to the active window.

Copyright (C) 2003 Ollie Rutherfurd <oliver@rutherfurd.net>

Python License

Version 0.5.1 (2017-12-31)

$Id$
"""

import sys
import time
import ctypes
import typing

from _sendkeys import key_up, key_down, toggle_numlock

from threading import Lock

from ctypes import c_uint8, c_int, c_uint, c_short, WinDLL, create_unicode_buffer, POINTER
from ctypes.wintypes import WORD, DWORD, LPWSTR, WCHAR, LONG

__all__ = ['KeySequenceError', 'SendKeys']

user32 = WinDLL('user32', use_last_error=True)

ULONG_PTR = POINTER(DWORD)


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (('wVk', WORD),
                ('wScan', WORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))


# Included for completeness.
class MOUSEINPUT(ctypes.Structure):
    _fields_ = (('dx', LONG),
                ('dy', LONG),
                ('mouseData', DWORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (('wVk', WORD),
                ('wScan', WORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (('uMsg', DWORD),
                ('wParamL', WORD),
                ('wParamH', WORD))


class _INPUTunion(ctypes.Union):
    _fields_ = (('mi', MOUSEINPUT),
                ('ki', KEYBDINPUT),
                ('hi', HARDWAREINPUT))


class INPUT(ctypes.Structure):
    _fields_ = (('type', DWORD),
                ('union', _INPUTunion))

MapVirtualKey = user32.MapVirtualKeyW
MapVirtualKey.argtypes = [c_uint, c_uint]
MapVirtualKey.restype = c_uint

keyboard_state_type = c_uint8 * 256

ToUnicode = user32.ToUnicode
ToUnicode.argtypes = [c_uint, c_uint, keyboard_state_type, LPWSTR, c_int, c_uint]
ToUnicode.restype = c_int

VkKeyScan = user32.VkKeyScanW
VkKeyScan.argtypes = [WCHAR]
VkKeyScan.restype = c_short

SendInput = user32.SendInput
SendInput.argtypes = [c_uint, POINTER(INPUT), c_int]
SendInput.restype = c_uint

KEYEVENTF_KEYUP = 0x02
KEYEVENTF_UNICODE = 0x04

INPUT_KEYBOARD = 1

USER32_MAPVK_VK_TO_VSC = 0
USER32_MAPVK_VSC_TO_VK = 1

VK_SHIFT = 0x10
VK_CONTROL = 0x11
VK_MENU = 0x12
ALT_GR = 0xA5  # RIGHT_MENU

PAUSE = 50 / 1000.0  # 50 milliseconds

# imported from 'WinUser.h'
CODES = {
    "LBUTTON": 0x01,
    "RBUTTON": 0x02,
    "CANCEL": 0x03,
    "MBUTTON": 0x04,  # NOT contiguous with L & RBUTTON
    "XBUTTON1": 0x05,  # NOT contiguous with L & RBUTTON
    "XBUTTON2": 0x06,  # NOT contiguous with L & RBUTTON
    "BACK": 0x08,
    "TAB": 0x09,
    "\t": 0x09,
    "CLEAR": 0x0C,
    "RETURN": 0x0D,
    "ENTER": 0x0D,
    "\n": 0x0D,
    "\r": 0x0D,
    "SHIFT": VK_SHIFT,
    "CONTROL": VK_CONTROL,
    "CTRL": VK_CONTROL,
    "MENU": VK_MENU,
    "ALT": VK_MENU,
    "PAUSE": 0x13,
    "CAPITAL": 0x14,
    "KANA": 0x15,
    "HANGEUL": 0x15,  # old name - should be here for compatibility
    "HANGUL": 0x15,
    "JUNJA": 0x17,
    "FINAL": 0x18,
    "HANJA": 0x19,
    "KANJI": 0x19,
    "ESCAPE": 0x1B,
    "CONVERT": 0x1C,
    "NONCONVERT": 0x1D,
    "ACCEPT": 0x1E,
    "MODECHANGE": 0x1F,
    "SPACE": 0x20,
    "PRIOR": 0x21,
    "NEXT": 0x22,
    "END": 0x23,
    "HOME": 0x24,
    "LEFT": 0x25,
    "UP": 0x26,
    "RIGHT": 0x27,
    "DOWN": 0x28,
    "SELECT": 0x29,
    "PRINT": 0x2A,
    "EXECUTE": 0x2B,
    "SNAPSHOT": 0x2C,
    "INSERT": 0x2D,
    "DELETE": 0x2E,
    "HELP": 0x2F,
    "LWIN": 0x5B,
    "RWIN": 0x5C,
    "APPS": 0x5D,
    "SLEEP": 0x5F,
    "NUMPAD0": 0x60,
    "NUMPAD1": 0x61,
    "NUMPAD2": 0x62,
    "NUMPAD3": 0x63,
    "NUMPAD4": 0x64,
    "NUMPAD5": 0x65,
    "NUMPAD6": 0x66,
    "NUMPAD7": 0x67,
    "NUMPAD8": 0x68,
    "NUMPAD9": 0x69,
    "MULTIPLY": 0x6A,
    "ADD": 0x6B,
    "SEPARATOR": 0x6C,
    "SUBTRACT": 0x6D,
    "DECIMAL": 0x6E,
    "DIVIDE": 0x6F,
    "F1": 0x70,
    "F2": 0x71,
    "F3": 0x72,
    "F4": 0x73,
    "F5": 0x74,
    "F6": 0x75,
    "F7": 0x76,
    "F8": 0x77,
    "F9": 0x78,
    "F10": 0x79,
    "F11": 0x7A,
    "F12": 0x7B,
    "F13": 0x7C,
    "F14": 0x7D,
    "F15": 0x7E,
    "F16": 0x7F,
    "F17": 0x80,
    "F18": 0x81,
    "F19": 0x82,
    "F20": 0x83,
    "F21": 0x84,
    "F22": 0x85,
    "F23": 0x86,
    "F24": 0x87,
    "NUMLOCK": 0x90,
    "SCROLL": 0x91,
    "OEM_NEC_EQUAL": 0x92,  # '=' key on numpad
    "OEM_FJ_JISHO": 0x92,  # 'Dictionary' key
    "OEM_FJ_MASSHOU": 0x93,  # 'Unregister word' key
    "OEM_FJ_TOUROKU": 0x94,  # 'Register word' key
    "OEM_FJ_LOYA": 0x95,  # 'Left OYAYUBI' key
    "OEM_FJ_ROYA": 0x96,  # 'Right OYAYUBI' key
    "LSHIFT": 0xA0,
    "RSHIFT": 0xA1,
    "LCONTROL": 0xA2,
    "RCONTROL": 0xA3,
    "LMENU": 0xA4,
    "RMENU": ALT_GR,
    "ALTGR": ALT_GR,
    "BROWSER_BACK": 0xA6,
    "BROWSER_FORWARD": 0xA7,
    "BROWSER_REFRESH": 0xA8,
    "BROWSER_STOP": 0xA9,
    "BROWSER_SEARCH": 0xAA,
    "BROWSER_FAVORITES": 0xAB,
    "BROWSER_HOME": 0xAC,
    "VOLUME_MUTE": 0xAD,
    "VOLUME_DOWN": 0xAE,
    "VOLUME_UP": 0xAF,
    "MEDIA_NEXT_TRACK": 0xB0,
    "MEDIA_PREV_TRACK": 0xB1,
    "MEDIA_STOP": 0xB2,
    "MEDIA_PLAY_PAUSE": 0xB3,
    "LAUNCH_MAIL": 0xB4,
    "LAUNCH_MEDIA_SELECT": 0xB5,
    "LAUNCH_APP1": 0xB6,
    "LAUNCH_APP2": 0xB7,
    "OEM_1": 0xBA,  # ';:' for US
    "OEM_PLUS": 0xBB,  # '+' any country
    "OEM_COMMA": 0xBC,  # ',' any country
    "OEM_MINUS": 0xBD,  # '-' any country
    "OEM_PERIOD": 0xBE,  # '.' any country
    "OEM_2": 0xBF,  # '/?' for US
    "OEM_3": 0xC0,  # '`~' for US
    "OEM_4": 0xDB,  # '[{' for US
    "OEM_5": 0xDC,  # '\|' for US
    "OEM_6": 0xDD,  # ']}' for US
    "OEM_7": 0xDE,  # ''"' for US
    "OEM_8": 0xDF,
    "OEM_AX": 0xE1,  # 'AX' key on Japanese AX kbd
    "OEM_102": 0xE2,  # "<>" or "\|" on RT 102-key kbd.
    "ICO_HELP": 0xE3,  # Help key on ICO
    "ICO_00": 0xE4,  # 00 key on ICO
    "PROCESSKEY": 0xE5,
    "ICO_CLEAR": 0xE6,
    "PACKET": 0xE7,
    "OEM_RESET": 0xE9,
    "OEM_JUMP": 0xEA,
    "OEM_PA1": 0xEB,
    "OEM_PA2": 0xEC,
    "OEM_PA3": 0xED,
    "OEM_WSCTRL": 0xEE,
    "OEM_CUSEL": 0xEF,
    "OEM_ATTN": 0xF0,
    "OEM_FINISH": 0xF1,
    "OEM_COPY": 0xF2,
    "OEM_AUTO": 0xF3,
    "OEM_ENLW": 0xF4,
    "OEM_BACKTAB": 0xF5,
    "ATTN": 0xF6,
    "CRSEL": 0xF7,
    "EXSEL": 0xF8,
    "EREOF": 0xF9,
    "PLAY": 0xFA,
    "ZOOM": 0xFB,
    "NONAME": 0xFC,
    "PA1": 0xFD,
    "OEM_CLEAR": 0xFE,
}


PAUSE_CMD = "PAUSE="


class VirtualKey:
    __slots__ = (
        "code",
        "shift",
        "altgr",
        "extended",
        "keypad"
    )

    def __init__(self, code: int,
                 shift: bool, altgr: bool,
                 extended: bool, keypad: bool):
        self.code = code
        self.shift = shift
        self.altgr = altgr
        self.extended = extended
        self.keypad = keypad


class KeySequenceError(Exception):
    """Exception raised when a key sequence string has a syntax error"""

    def __str__(self):
        return ' '.join(self.args)


class Layout:
    DEFAULT_FLAG = 0x0
    IS_DEAD_KEY = 0x1
    REQUIRES_SHIFT = 0x2
    REQUIRES_ALT_GR = 0x4

    __slots__ = (
        "_chars_to_scancodes",
        "_vk_to_scancode",
        "_scan_code_to_vk",
        "lock"
    )

    def __init__(self):
        self._chars_to_scancodes = {}
        self._vk_to_scancode = {}
        self._scan_code_to_vk = {}
        self.lock = Lock()

    @property
    def chars_to_scancodes(self):
        return self._chars_to_scancodes

    @property
    def vk_to_scancode(self):
        return self._vk_to_scancode

    @property
    def scan_code_to_vk(self):
        return self._scan_code_to_vk

    def add_scancode_to_vk(self, scancode, vk):
        self._scan_code_to_vk[scancode] = vk
        self._vk_to_scancode[vk] = scancode

    def associate_char_to_scancode(self, char, scancode, vk, flags=0):
        self._chars_to_scancodes[char] = (scancode, flags)
        if vk is not None:
            self.add_scancode_to_vk(scancode, vk)

    def char2keycode(self, c) -> typing.Tuple[int, int]:
        scancode, flags = self._chars_to_scancodes[c]
        return self._scan_code_to_vk[scancode], flags

    def key_to_code(self, key) -> typing.Tuple[int, int]:
        # the key is a char, try to get a scan code for it
        try:
            if len(key) == 1:
                return self.char2keycode(key)
        except KeyError:
            pass

        # try to get the key from the constant VirtualKeys
        if key in CODES:
            return CODES[key], Layout.DEFAULT_FLAG

        # finally try to get from the scanned and found VirtualKeys
        # associated with a scan code
        if key in self.vk_to_scancode:
            return self.vk_to_scancode[key], Layout.DEFAULT_FLAG

        # if we didn't found anything, raise exception
        raise KeySequenceError("'{}' is an unknown key".format(key))


def _setup_tables():
    """
    Ensures the scan code/virtual key code/name translation tables are
    filled.
    """

    layout = Layout()

    with layout.lock:
        for vk in range(0x01, 0x100):
            if vk not in layout.vk_to_scancode:
                scan_code = MapVirtualKey(vk, USER32_MAPVK_VK_TO_VSC)
                if scan_code and scan_code not in layout.vk_to_scancode:
                    layout.add_scancode_to_vk(scan_code, vk)

        name_buffer = create_unicode_buffer(32)
        keyboard_state = keyboard_state_type()
        for scan_code in range(2 ** (23-16)):
            # Get associated character, such as "^", possibly overwriting the pure key name.
            modifiers_to_scan = ((VK_SHIFT, Layout.REQUIRES_SHIFT), (ALT_GR, Layout.REQUIRES_ALT_GR))
            for state in [0, 1]:
                for vk_state, state_flag in modifiers_to_scan:
                    keyboard_state[vk_state] = state * 0xFF

                    # Try both manual and automatic scan_code->vk translations.
                    vk = user32.MapVirtualKeyW(scan_code, 3)
                    ret = ToUnicode(vk, scan_code, keyboard_state, name_buffer, len(name_buffer), 0)

                    if ret:
                        char = name_buffer.value[-1]

                        if char not in layout.chars_to_scancodes:
                            layout.associate_char_to_scancode(char, scan_code, vk, state and state_flag or 0)

                    # remove the hold
                    keyboard_state[vk_state] = 0 * 0xFF
    return layout


def _parse_pause_key(key: str):
    if len(key) > len(PAUSE_CMD) and key.startswith(PAUSE_CMD):
        try:
            res = float(key[len(PAUSE_CMD):])
        except ValueError:
            raise KeySequenceError("Invalid argument: '{}' for '{}'".format(res, PAUSE_CMD))
        return None, res


def _append_char(keys, c, layout: Layout):
    try:
        res = layout.key_to_code(c)
        _append_key(res, keys)
    except KeySequenceError:
        keys.append((c, True))


def _append_key(virtual_key, output, down=True, up=True):
    return _append_keys([virtual_key], output, down, up)


def _append_keys(virtual_keys, output, down=True, up=True):
    def _handle_flag(_vk, _flag):
        if (_flag & Layout.REQUIRES_SHIFT) == Layout.REQUIRES_SHIFT:
            return [VK_SHIFT]
        elif (_flag & Layout.REQUIRES_ALT_GR) == Layout.REQUIRES_ALT_GR:
            return [ALT_GR]
        return []

    def _append(_actions, _state, _out):
        _out +=  [(_action, _state) for _action in _actions]

    for vk, flag in virtual_keys:
        actions = _handle_flag(vk, flag)
        if down:
            _append(actions, True, output)
            output.append((vk, True))
        if up:
            output.append((vk, False))
            _append(actions, False, output)


def _peek_char(s: str, pos: int) -> str:
    if pos >= len(s):
        return None
    return s[pos]


def _parse_multiplier(s: str, pos: int) -> (int, int):
    chars = []
    c = None
    while True:
        pos += 1
        if len(s) < pos:
            raise KeySequenceError("Was expecting ']'")

        c = s[pos]

        if c == "]":
            break

        if not c.isdigit():
            raise KeySequenceError("Multiplier must be integer")
        chars.append(c)

    return int(''.join(chars)), pos + 1  # +1 because of `]`


def _parse_combo(s: str, pos: int, layout: Layout) -> (int, int):
    keys = []
    keys_up = []
    keys_down = []

    current_key_chars = []
    next_is_raw = False
    multiplier = 1

    while True:
        pos += 1
        if len(s) < pos:
            raise KeySequenceError("Was expecting '}'")

        c = s[pos]
        if next_is_raw:
            current_key_chars.append(c)
            next_is_raw = False
        elif c == '\\':
            next_is_raw = True
        elif c == "[":
            multiplier, pos = _parse_multiplier(s, pos)
            next_c = _peek_char(s, pos)
            pos -= 1  # restore the cursor to the position of ']'
            if next_c not in ("+", "}"):
                raise KeySequenceError("Was expecting '}'")
        elif c == "+" or c == "}":
            found_key = ''.join(current_key_chars)
            if not found_key:
                raise KeySequenceError("Was expecting a key, got nothing instead")

            pause_cmd = _parse_pause_key(found_key)
            if pause_cmd:
                keys_up += [pause_cmd] * multiplier
            else:
                vk = layout.key_to_code(found_key)

                # append the found key and multiply it by the given multiplier or by one
                # if the multiplier is not one, we switch the status between DOWN and UP.
                #
                # It is there for limited cases, that would allow users to send multiple times
                # a letter while holding another key.
                #
                # Example: {SHIFT+A[2]} -> SHIFT DOWN, A DOWN, A UP, A DOWN, A UP, SHIFT UP
                # Example: {SHIFT+A[2]+E[2]} -> would type: AAEE
                #
                # For cases of simple combo,
                # example: {ALT+TAB} would do: ALT DOWN, TAB DOWN, ALT UP, TAB UP.
                #
                # Which means:
                #    `multiplier == 1` -> before (down) and after (up) `multiplier > 1`
                if multiplier != 1:
                    for i in range(multiplier):
                        _append_key(vk, keys)
                else:
                    _append_key(vk, keys_down, True, False)
                    _append_key(vk, keys_up, False, True)

            # reset values
            current_key_chars = []
            multiplier = 1

            # stop there
            if c == "}":
                break
        else:
            current_key_chars.append(c)

    pos += 1
    keys = keys_down + keys + keys_up

    # if next char is "[", multiply the value by the given one
    next_c = _peek_char(s, pos)
    if next_c == "[":
        multiplier, pos = _parse_multiplier(s, pos)
        keys *= multiplier

    return keys, pos


def str2keys(key_string,
             layout: Layout,
             with_spaces=False,
             with_tabs=False,
             with_newlines=False
             ):
    """
    Converts `key_string` string to a list of 2-tuples,
    ``(keycode,down)``, which  can be given to `playkeys`.

    `key_string` : str
        A string of keys.
    `with_spaces` : bool
        Whether to treat spaces as ``{SPACE}``. If `False`, spaces are ignored.
    `with_tabs` : bool
        Whether to treat tabs as ``{TAB}``. If `False`, tabs are ignored.
    `with_newlines` : bool
        Whether to treat newlines as ``{ENTER}``. If `False`, newlines are ignored.
    """

    # remove any ignored character
    if not (with_spaces and with_tabs and with_newlines):
        ignored_chars = (' ' if not with_spaces else '')\
                        + ('\t' if not with_tabs else '') \
                        + ('\n' if not with_newlines else '')

        chars = []
        for c in key_string:
            if c not in ignored_chars:
                chars.append(c)

        key_string = ''.join(chars)
        del chars, ignored_chars

    # vars
    pos = 0
    next_is_raw = False

    # results
    keys = []

    while pos < len(key_string):
        c = key_string[pos]

        if next_is_raw:
            _append_char(keys, c, layout)
            next_is_raw = False
        elif c == "{":
            combo_keys, pos = _parse_combo(key_string, pos, layout)
            keys += combo_keys
            continue
        elif c == "\\":
            next_is_raw = True
        else:
            _append_char(keys, c, layout)

        pos += 1

    return keys


def _send_event(vk, event_type, layout: Layout):
    if vk < 0:
        code = -vk
        vk = layout.scan_code_to_vk.get(code, 0)
    else:
        code = layout.vk_to_scancode[vk]
    user32.keybd_event(vk, code, event_type, 0)


def press(code, layout: Layout):
    _send_event(code, 0, layout)


def release(code, layout: Layout):
    _send_event(code, 2, layout)


# thanks to: https://github.com/boppreh/keyboard!
def type_unicode(character):
    # This code and related structures are based on
    # http://stackoverflow.com/a/11910555/252218
    inputs = []
    surrogates = bytearray(character.encode('utf-16le'))
    for i in range(0, len(surrogates), 2):
        higher, lower = surrogates[i:i+2]
        structure = KEYBDINPUT(0, (lower << 8) + higher, KEYEVENTF_UNICODE, 0, None)
        inputs.append(INPUT(INPUT_KEYBOARD, _INPUTunion(ki=structure)))
    nInputs = len(inputs)
    LPINPUT = INPUT * nInputs
    pInputs = LPINPUT(*inputs)
    cbSize = c_int(ctypes.sizeof(INPUT))
    SendInput(nInputs, pInputs, cbSize)


def playkeys(keys, layout: Layout, pause=.05):
    """
    Simulates pressing and releasing one or more keys.

    `keys` : str
        A list of 2-tuples consisting of ``(keycode,down)``
        where `down` is `True` when the key is being pressed
        and `False` when it's being released.

        `keys` is returned from `str2keys`.
    `pause` : float
        Number of seconds between releasing a key and pressing the
        next one.
    """
    def handle_flag(_flag, _callback):
        if (_flag & Layout.REQUIRES_SHIFT) == Layout.REQUIRES_SHIFT:
            _callback(VK_SHIFT)
        elif (_flag & Layout.REQUIRES_ALT_GR) == Layout.REQUIRES_ALT_GR:
            _callback(ALT_GR)

    for (vk, arg) in keys:
        if vk:
            if type(vk) is str:
                type_unicode(vk)
            else:
                if arg:
                    press(vk, layout)
                else:
                    release(vk, layout)
                    if pause:  # pause after key up
                        time.sleep(pause)
        else:
            time.sleep(arg)


def SendKeys(keys,
             layout: Layout=None,
             pause=0.05,
             with_spaces=False,
             with_tabs=False,
             with_newlines=False,
             turn_off_numlock=True):
    """
    Sends keys to the current window.

    `keys` : str
        A string of keys.
    `pause` : float
        The number of seconds to wait between sending each key
        or key combination.
    `with_spaces` : bool
        Whether to treat spaces as ``{SPACE}``. If `False`, spaces are ignored.
    `with_tabs` : bool
        Whether to treat tabs as ``{TAB}``. If `False`, tabs are ignored.
    `with_newlines` : bool
        Whether to treat newlines as ``{ENTER}``. If `False`, newlines are ignored.
    `turn_off_numlock` : bool
        Whether to turn off `NUMLOCK` before sending keys.

    example::

        SendKeys("Hello{SPACE}World!")

    would result in ``"Hello World!"``
    """

    if layout is None:
        layout = _setup_tables()

    restore_numlock = False
    try:
        # read keystroke keys into a list of 2 tuples [(key,up),]
        _keys = str2keys(keys, layout, with_spaces, with_tabs, with_newlines)

        # certain keystrokes don't seem to behave the same way if NUMLOCK
        # is on (for example, ^+{LEFT}), so turn NUMLOCK off, if it's on
        # and restore its original state when done.
        if turn_off_numlock:
            restore_numlock = toggle_numlock(False)

        # "play" the keys to the active window
        playkeys(_keys, layout, pause)
    finally:
        if restore_numlock and turn_off_numlock:
            key_down(CODES['NUMLOCK'])
            key_up(CODES['NUMLOCK'])


def usage():
    """
    Writes help message to `stderr` and exits.
    """
    print("""\
%(name)s [-h] [-d seconds] [-p seconds] [-f filename] or [string of keys]

    -dN    or --delay=N   : N is seconds before starting
    -pN    or --pause=N   : N is seconds between each key
    -fNAME or --file=NAME : NAME is filename containing keys to send
    -h     or --help      : show help message"""
          % {'name': 'SendKeys.py'},
          file=sys.stderr)
    sys.exit(1)


def error(msg):
    """
    Writes `msg` to `stderr`, displays usage
    information, and exits.
    """
    print('\nERROR: %s\n' % msg, file=sys.stderr)
    usage()


def main(args=None):
    import getopt

    if args is None:
        args = sys.argv[1:]

    try:
        opts, args = getopt.getopt(args,
                                   "hp:d:f:", ["help", "pause", "delay", "file"])
    except getopt.GetoptError:
        usage()

    pause = 0
    delay = 0
    filename = None

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
        elif o in ('-f', '--file'):
            filename = a
        elif o in ('-p', '--pause'):
            try:
                pause = float(a)
                assert pause >= 0
            except (ValueError, AssertionError) as e:
                error('`pause` must be >= 0.0')
        elif o in ('-d', '--delay'):
            try:
                delay = float(a)
                assert delay >= 0
            except (ValueError, AssertionError) as e:
                error('`delay` must be >= 0.0')

    time.sleep(delay)

    if filename is not None and args:
        error("can't pass both filename and string of keys on command-line")
    elif filename:
        f = open(filename)
        keys = f.read()
        f.close()
        SendKeys(keys, pause)
    else:
        for a in args:
            SendKeys(a, pause)


if __name__ == '__main__':
    main(sys.argv[1:])
