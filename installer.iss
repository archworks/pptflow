#ifndef MyAppVersion
#define MyAppVersion "v1.0.0"
#endif
; 定义安装包的基本信息
[Setup]
AppName=PPTFlow
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\ArchWorks PPTFlow 2025
DefaultGroupName=PPTFlow
OutputBaseFilename=pptflow-{#MyAppVersion}
Compression=lzma
SolidCompression=yes
DisableProgramGroupPage=yes
DisableDirPage=no
SetupIconFile=assets\icons\pptflow.ico

[Files]
; 将 PyInstaller 打包的可执行文件复制到安装目录
Source: "dist\pptflow\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; 创建桌面快捷方式
Name: "{commondesktop}\PPTFlow"; Filename: "{app}\pptflow.exe"; WorkingDir: "{app}"; IconFilename: "{app}\_internal\assets\icons\pptflow.ico"
; 创建开始菜单快捷方式
Name: "{group}\PPTFlow"; Filename: "{app}\pptflow.exe"; WorkingDir: "{app}"; IconFilename: "{app}\_internal\assets\icons\pptflow.ico"

[Run]
; 安装完成后运行程序（可选）
Filename: "{app}\pptflow.exe"; Description: "启动 PPTFlow"; Flags: nowait postinstall skipifsilent

; 安装过程的定制文本
[Messages]
SetupAppTitle=PPTFlow 安装程序
SetupWindowTitle=安装 PPTFlow

[UninstallDelete]
; 卸载时删除安装目录下的所有文件和目录
Type: filesandordirs; Name: "{app}"
