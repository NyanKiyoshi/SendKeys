from SendKeys import SendKeys

SendKeys("{LWIN+r}Notepad.exe\n", pause=.1, with_newlines=True)
SendKeys("\"#()", pause=.05)
SendKeys("{ALT+TAB}[2]", pause=.5)
SendKeys("()}\{{ENTER}", pause=.01)
SendKeys("coucou, je support désormais l'unicode :D ♥{ENTER}", pause=.05, with_spaces=True)
SendKeys("{ALT+F}{X}{PAUSE=0.4}n")
