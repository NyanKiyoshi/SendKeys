"""
SendKeys.py - Sends one or more keystroke or keystroke combinations
to the active window.

Copyright (C) 2003 Ollie Rutherfurd <oliver@rutherfurd.net>

Python License

Version 0.3 (2003-06-14)

$Id$
"""

import sys
import time
from _sendkeys import char2keycode, key_up, key_down, toggle_numlock

__all__ = ['KeySequenceError', 'SendKeys']

KEYEVENTF_KEYUP = 0x02
VK_SHIFT = 0x10
VK_CONTROL = 0x11
VK_MENU = 0x12

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
    "CLEAR": 0x0C,
    "RETURN": 0x0D,
    "ENTER": 0x0D,
    "\n": 0x0D,
    "SHIFT": 0x10,
    "CONTROL": 0x11,
    "CTRL": 0x11,
    "MENU": 0x12,
    "ALT": 0x12,
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
    "RMENU": 0xA5,
    "ALTGR": 0xA5,
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


US_LAYOUT_CHARS_SHIFT = {
    '!': '1',
    '@': '2',
    '#': '3',
    '$': '4',
    '&': '7',
    '*': '8',
    '_': '-',
    '|': '\\',
    ':': ';',
    '"': '\'',
    '<': ',',
    '>': '.',
    '?': '/',
}


UK_LAYOUT_CHARS_SHIFT = {
    '¬': '`',
    '!': '1',
    '"': '2',
    '£': '3',
    '$': '4',
    '%': '5',
    '^': '6',
    '&': '7',
    '*': '8',
    '(': '9',
    ')': '0',
    '_': '-',
    '+': '=',
    '{': '[',
    '}': ']',
    ':': ';',
    '@': '\'',
    '~': '#',
    '<': ',',
    '>': '.',
    '?': '/',
    '|': '\\',
}


PAUSE_CMD = "PAUSE="


class KeySequenceError(Exception):
    """Exception raised when a key sequence string has a syntax error"""

    def __str__(self):
        return ' '.join(self.args)


def _parse_pause_key(key: str):
    if len(key) > len(PAUSE_CMD) and key.startswith(PAUSE_CMD):
        try:
            res = float(key[len(PAUSE_CMD):])
        except ValueError:
            raise KeySequenceError("Invalid argument: '{}' for '{}'".format(res, PAUSE_CMD))
        return None, res


# TODO: implement layout selection/ autoselection
def _append_char(keys, c, layout=None):
    res = key_to_code(c)
    to_append = [(res, True), (res, False)]
    if c.isupper() or c in UK_LAYOUT_CHARS_SHIFT:
        to_append = [(VK_SHIFT, True)] + to_append + [(VK_SHIFT, False)]
    keys += to_append


def key_to_code(key):
    if len(key) == 1:
        return char2keycode(key.encode('utf-8'))
    if key in CODES:
        return CODES[key]
    raise KeySequenceError("'{}' is an unknown key".format(key))


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


def _parse_combo(s: str, pos: int) -> (int, int):
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
                keys += [pause_cmd] * multiplier
            else:
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
                        for status in (True, False):
                            keys.append((key_to_code(found_key), status))
                else:
                    keys_down += [(key_to_code(found_key), True)]
                    keys_up += [(key_to_code(found_key), False)]

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
             with_spaces=False,
             with_tabs=False,
             with_newlines=False):
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
            _append_char(keys, c)
            next_is_raw = False
        elif c == "{":
            combo_keys, pos = _parse_combo(key_string, pos)
            keys += combo_keys
            continue
        elif c == "\\":
            next_is_raw = True
        else:
            _append_char(keys, c)

        pos += 1

    return keys


def playkeys(keys, pause=.05):
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
    for (vk, arg) in keys:
        if vk:
            if arg:
                key_down(vk)
            else:
                key_up(vk)
                if pause:  # pause after key up
                    time.sleep(pause)
        else:
            time.sleep(arg)


def SendKeys(keys,
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

        SendKeys("+hello{SPACE}+world+1")

    would result in ``"Hello World!"``
    """

    restore_numlock = False
    try:
        # read keystroke keys into a list of 2 tuples [(key,up),]
        _keys = str2keys(keys, with_spaces, with_tabs, with_newlines)

        # certain keystrokes don't seem to behave the same way if NUMLOCK
        # is on (for example, ^+{LEFT}), so turn NUMLOCK off, if it's on
        # and restore its original state when done.
        if turn_off_numlock:
            restore_numlock = toggle_numlock(False)

        # "play" the keys to the active window
        playkeys(_keys, pause)
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

    if not filename is None and args:
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
