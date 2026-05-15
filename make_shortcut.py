# make_shortcut.py
import os
import winshell
from win32com.client import Dispatch

desktop = winshell.desktop()
shortcut_path = os.path.join(desktop, "InfoNote.lnk")

project_path = os.path.dirname(os.path.abspath(__file__))
tray_path = os.path.join(project_path, "tray.py")
icon_path = os.path.join(project_path, "choco.ico")

shell = Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut(shortcut_path)
shortcut.Targetpath = "pythonw"
shortcut.Arguments = f'"{tray_path}"'
shortcut.WorkingDirectory = project_path
shortcut.IconLocation = icon_path
shortcut.save()

print("완료! 바탕화면에 InfoNote.lnk 생성됨")
