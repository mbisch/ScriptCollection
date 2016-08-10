Set WSHShell = WScript.CreateObject("WScript.Shell")
Set WshEnv = WshShell.Environment("USER")
WshEnv("AMBIT_CIM_OUT_DIR") = "C:\Projekte\windekis_appl"