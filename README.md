# ScreenResizer

Simple Windows utility to list displays and change the selected display's resolution.

Usage

- Run with Python 3 on Windows. For resolution changes, run as an Administrator if required by your system.
- From the workspace root:

```powershell
python c:\ScreenResizer\main.py
```

Notes

- This tool uses Windows APIs via `ctypes` to enumerate displays and modes and to call `ChangeDisplaySettingsEx`.
- Changing display settings may momentarily alter or disrupt the desktop. Use with caution.
