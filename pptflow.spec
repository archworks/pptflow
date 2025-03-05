# -*- mode: python ; coding: utf-8 -*-

import sys
import os
import azure.cognitiveservices.speech
import language_tags.data
import espeakng_loader
from PyInstaller.utils.hooks import collect_data_files

# 动态选择平台库文件
if sys.platform == 'darwin':
    AZURE_LIB_FILE = 'libMicrosoft.CognitiveServices.Speech.core.dylib'
    ICON_FILE = 'assets/icons/pptflow.icns'
elif sys.platform == 'win32':
    AZURE_LIB_FILE = 'Microsoft.CognitiveServices.Speech.core.dll'
    ICON_FILE = 'assets/icons/pptflow.ico'
else:
    AZURE_LIB_FILE = 'libMicrosoft.CognitiveServices.Speech.core.so'
    ICON_FILE = 'assets/icons/pptflow.ico'

azure_lib = os.path.join(os.path.dirname(azure.cognitiveservices.speech.__file__), AZURE_LIB_FILE)
language_tags = os.path.join(os.path.dirname(language_tags.data.__file__), 'json')
espeakng_loader = os.path.dirname(espeakng_loader.__file__)
# 分析主脚本和依赖
a = Analysis(
    ['main.py'],  # 主入口文件
    pathex=[],  # 搜索路径
    binaries=[],  # 二进制文件（自动检测）
    datas=[
        # 添加资源文件（格式：(源路径, 目标路径)）
        (azure_lib, 'azure/cognitiveservices/speech'),
        ('pptflow/locales', 'pptflow/locales'),
        ('assets', 'assets'),
        ('model', 'model'),
        (language_tags, 'language_tags/data/json/'),
        (espeakng_loader, 'espeakng_loader/'),
    ],
    hiddenimports=[
        'azure.cognitiveservices.speech',  # 显式隐藏导入
    ],
    hookspath=[],  # 自定义钩子路径
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='pptflow',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[ICON_FILE],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='pptflow',
)
app = BUNDLE(
    coll,
    name='pptflow.app',
    icon=ICON_FILE,
    bundle_identifier=None,
)