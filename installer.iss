; Inno Setup script to create an installer for the ScreenResizerTool
[Setup]
AppName=ScreenResizerTool
AppVersion=1.0
DefaultDirName={pf}\ScreenResizerTool
DefaultGroupName=ScreenResizerTool
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\\main.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\ScreenResizerTool"; Filename: "{app}\main.exe"

[Run]
Filename: "{app}\main.exe"; Description: "Launch ScreenResizerTool"; Flags: nowait postinstall skipifsilent
