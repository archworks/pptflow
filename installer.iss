#define MyAppVersion "1.0.0"
; 定义安装包的基本信息
[Setup]
AppName=PPTFlow
AppVersion={#MyAppVersion}
DefaultDirName={pf}\PPTFlow
DefaultGroupName=PPTFlow
OutputBaseFilename=pptflow-{#MyAppVersion}-alpha
Compression=lzma
SolidCompression=yes
DisableProgramGroupPage=yes

[Files]
; 将 PyInstaller 打包的可执行文件复制到安装目录
Source: "dist\pptflow.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; 创建桌面快捷方式
Name: "{commondesktop}\PPTFlow"; Filename: "{app}\pptflow.exe"; WorkingDir: "{app}"
; 创建开始菜单快捷方式
Name: "{group}\PPTFlow"; Filename: "{app}\pptflow.exe"; WorkingDir: "{app}"

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
