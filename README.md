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

## Packaging (Windows executable)

You can build a single-file Windows executable using PyInstaller and optionally create a native installer using Inno Setup.

- **Build with PyInstaller (one-file exe):**

	From the workspace root, run:

	```powershell
	.\build.bat
	```

	After the script completes the executable will be in the `dist` folder as `main.exe`.

- **Create an installer (Inno Setup):**

	1. Install Inno Setup from https://jrsoftware.org/
	2. Open `installer.iss` in Inno Setup and compile. It expects the executable at `dist\main.exe`.

Notes:

- Building an executable requires Python and network access to install `pyinstaller` and other dependencies.
- The resulting executable is a Windows binary; test on target machines. Some anti-virus products may flag unsigned executables.
