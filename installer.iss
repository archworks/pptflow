; 定义安装包的基本信息
[Setup]
AppName=PPTFlow           ; 应用程序名称
AppVersion=1.0.0          ; 版本号，可以从命令行传递动态版本
DefaultDirName={pf}\PPTFlow  ; 默认安装目录
DefaultGroupName=PPTFlow     ; 默认的开始菜单文件夹
OutputBaseFilename=PPTFlowInstaller ; 输出的安装包文件名
Compression=lzma            ; 压缩算法
SolidCompression=yes        ; 启用固体压缩
DisableProgramGroupPage=yes ; 隐藏“选择开始菜单文件夹”页面
UninstallDisplayIcon={app}\PPTFlow.exe ; 卸载程序图标

[Files]
; 将 PyInstaller 打包的可执行文件复制到安装目录
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion

; 复制其他需要的文件（如 .env 文件）
Source: ".env"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; 创建桌面快捷方式
Name: "{commondesktop}\PPTFlow"; Filename: "{app}\main.exe"; WorkingDir: "{app}"
; 创建开始菜单快捷方式
Name: "{group}\PPTFlow"; Filename: "{app}\main.exe"; WorkingDir: "{app}"

[Run]
; 安装完成后运行程序（可选）
Filename: "{app}\main.exe"; Description: "启动 PPTFlow"; Flags: nowait postinstall skipifsilent

; 安装过程的定制文本
[Messages]
SetupAppTitle=PPTFlow 安装程序
SetupWindowTitle=安装 PPTFlow

[UninstallDelete]
; 卸载时删除安装目录下的所有文件和目录
Type: filesandordirs; Name: "{app}"
