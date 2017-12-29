from SendKeys import SendKeys

SendKeys("{LWIN+r}Notepad.exe\n{ALT+F}{X}", pause=.1, with_newlines=True)
SendKeys("{LWIN+r}Notepad.exe{ENTER}{PAUSE=0.4}{ALT+F}{X}", pause=.05)
SendKeys("{LWIN+r}\"#()", pause=.05)
