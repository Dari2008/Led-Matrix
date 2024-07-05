class KeyboardMap:

    KEY_LIST = [
        "ctrl",
        "shift",
        "alt",
        "alt gr",
        "caps lock"
        "command",
        "esc",
        "space",
        "backspace",
        "tab",
        "linefeed",
        "clear",
        "return",
        "pause",
        "scroll_lock",
        "sys_req",
        "delete",
        "home",
        "left",
        "up",
        "right",
        "down",
        "prior",
        "page_up",
        "next",
        "page_down",
        "end",
        "begin",
        "select",
        "print",
        "execute",
        "insert",
        "undo",
        "redo",
        "menu",
        "find",
        "cancel",
        "help",
        "break",
        "mode_switch",
        "script_switch",
        "num_lock",
        "F1",
        "F2",
        "F3",
        "F4",
        "F5",
        "F6",
        "F7",
        "F8",
        "F9",
        "F10",
        "F11",
        "L1",
        "F12",
        "L2",
        "F13",
        "L3",
        "F14",
        "L4",
        "F15",
        "L5",
        "F16",
        "L6",
        "F17",
        "L7",
        "F18",
        "L8",
        "F19",
        "L9",
        "F20",
        "L10",
        "F21",
        "R1",
        "F22",
        "R2",
        "F23",
        "R3",
        "F24",
        "R4",
        "F25",
        "R5",
        "F26",
        "R6",
        "F27",
        "R7",
        "F28",
        "R8",
        "F29",
        "R9",
        "F30",
        "R10",
        "F31",
        "R11",
        "F32",
        "R12",
        "F33",
        "R13",
        "F34",
        "R14",
        "F35",
        "R15",
        "A|a",
        "B|b",
        "C|c",
        "D|d",
        "E|e",
        "F|f",
        "G|g",
        "H|h",
        "I|i",
        "J|j",
        "K|k",
        "L|l",
        "M|m",
        "N|n",
        "O|o",
        "P|p",
        "Q|q",
        "R|r",
        "S|s",
        "T|t",
        "U|u",
        "V|v",
        "W|w",
        "X|x",
        "Y|y",
        "Z|z",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "\`",
        "~",
        "!",
        "@",
        "#",
        "$",
        "%",
        "^",
        "&",
        "*",
        "(",
        ")",
        "-",
        "_",
        "+",
        "=",
        "[",
        "]",
        "{",
        "}",
        "\\",
        "\""
        "|",
        ";",
        ":",
        "'",
        "/",
        "?",
        ".",
        ">",
        ",",
        "<",
        "ä",
        "ü",
        "ö",
    ]

    @staticmethod
    def getKey(key: str) -> int:
        try:
            key = KeyboardMap.KEY_LIST.index(key.lower())
        except:
            try:
                key = KeyboardMap.KEY_LIST.index(key.upper() + "|" + key.lower())
            except:
                try:
                    key = KeyboardMap.KEY_LIST.index(key.upper())
                except:
                    key = -1
        return key
    
    @staticmethod
    def getKeyName(key: int) -> str:
        return KeyboardMap.KEY_LIST[key]
    
    @staticmethod
    def getKeys() -> list:
        return KeyboardMap.KEY_LIST
    
    @staticmethod
    def getKeysDict() -> dict:
        return {key: KeyboardMap.KEY_LIST.index(key) for key in KeyboardMap.KEY_LIST}
    
    @staticmethod
    def getKeysDictReversed() -> dict:
        return {KeyboardMap.KEY_LIST.index(key): key for key in KeyboardMap.KEY_LIST}
    