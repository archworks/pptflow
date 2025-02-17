# -*- mode: python ; coding: utf-8 -*-

import sys
import os
import azure.cognitiveservices.speech
from PyInstaller.utils.hooks import collect_data_files

# 动态选择平台库文件（需根据实际文件路径调整）
if sys.platform == 'darwin':
    AZURE_LIB_FILE = 'libMicrosoft.CognitiveServices.Speech.core.dylib'
elif sys.platform == 'win32':
    AZURE_LIB_FILE = 'Microsoft.CognitiveServices.Speech.core.dll'
else:
    AZURE_LIB_FILE = 'libMicrosoft.CognitiveServices.Speech.core.so'

azure_lib = os.path.join(os.path.dirname(azure.cognitiveservices.speech.__file__), AZURE_LIB_FILE)
# 核心配置
block_cipher = None

# 分析主脚本和依赖
a = Analysis(
    ['main.py'],  # 主入口文件
    pathex=[os.getcwd()],  # 搜索路径
    binaries=[],  # 二进制文件（自动检测）
    datas=[
        # 添加资源文件（格式：(源路径, 目标路径)）
        (azure_lib, 'azure/cognitiveservices/speech'),
        ('pptflow/locales', 'pptflow/locales'),
        ('assets', 'assets'),
    ],
    hiddenimports=[
        'azure.cognitiveservices.speech',  # 显式隐藏导入
    ],
    hookspath=[],  # 自定义钩子路径
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],  # 排除无用模块以减少体积
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 配置 PY 压缩包（禁用 UPX）
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
    upx=False,  # 禁用 UPX
)

# 生成单文件 EXE
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='pptflow',  # 输出文件名
    debug=False,  # 禁用调试模式
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # 禁用 UPX
    runtime_tmpdir=None,
    console=False,  # 无控制台窗口（--windowed）
    disable_windowed_tracker=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,  # macOS 签名标识（可选）
    entitlements_file=None,  # macOS 权限文件（可选）
    icon='assets/icon.ico'  # 应用图标（可选）
)

app = BUNDLE(
    exe,
    name='pptflow.app',
    icon=None,
    bundle_identifier=None,
)
