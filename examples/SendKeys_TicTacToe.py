"""
Using SendKeys to play a game of Tic-Tac-Toe.

Ollie Rutherfurd <oliver@rutherfurd.net>

$Id$
"""

import tempfile
from SendKeys import SendKeys

if __name__ == "__main__":
    # create file game will be saved to
    filename = tempfile.mktemp(".txt")
    print("saving tic-tac-toe game to `%s`" % filename)

    with open(filename, 'w') as fp:
        fp.write('')

    # open notepad
    SendKeys(("{RWIN+r}Notepad.exe{SPACE}"
              "\"%(filename)s\""
              "{ENTER}{PAUSE=1}" % dict(filename=filename)).replace("\\", "\\\\"),
             with_spaces=True)

    # draw board
    SendKeys(
        "   |   |   \n"
        "---+---+---\n"
        "   |   |   \n"
        "---+---+---\n"
        "   |   |  ",

        pause=0.1,
        with_spaces=True,
        with_newlines=True
    )

    # play the game
    SendKeys(
        "{CTRL+HOME}"
        "{DOWN}[2]{RIGHT}[5]{SHIFT+RIGHT}{PAUSE=1}x"
        "{LEFT}[4]{SHIFT+LEFT}{SHIFT+o}"
        "{UP}[2]{RIGHT}[3]{SHIFT+RIGHT}x"
        "{DOWN}[4]{SHIFT+LEFT}{SHIFT+o}"
        "{LEFT}[4]{SHIFT+LEFT}x"
        "{RIGHT}[7]{UP}[4]{SHIFT+RIGHT}O"
        "{DOWN}[4]{SHIFT+LEFT}x"
        "{UP}[4]{LEFT}[8]{SHIFT+LEFT}{SHIFT+o}"
        "{RIGHT}[7]{DOWN}[2]{SHIFT+RIGHT}[1]x"
        "{CTRL+s}", 0.1
    )

    # read game saved from notepad
    with open(filename) as fp:
        output = fp.read()

    assert output == " O | x | O \n" \
                     "---+---+---\n" \
                     " O | x | x \n" \
                     "---+---+---\n" \
                     " x | O | x"

    print("Bad news: cat got the game")
    print("Good news: that's what we expected, so the test passed")
