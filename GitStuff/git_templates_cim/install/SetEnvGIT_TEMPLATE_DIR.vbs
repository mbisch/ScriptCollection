Set WSHShell = WScript.CreateObject("WScript.Shell")
Set WshEnv = WshShell.Environment("USER")
WshEnv("GIT_TEMPLATE_DIR") = "C:\Projekte\windekis_src\configuration\git_templates_cim"