# -*- mode: python ; coding: utf-8 -*-
import sys
import os

datas = [
    ('TerminalGameClient/assets/SFX', 'assets/SFX'),
    ('TerminalGameClient/assets/SFX', 'TerminalGameClient/assets/SFX'),
    ('assets/hub', 'assets/hub'),
]

hiddenimports = [
    'pygame',
    'rich',
    'rich.console',
    'rich.panel',
    'rich.table',
    'winsound',
    'random',
    'math',
    'time',
    'os',
    'sys',
    'characters',
    'characters.Models',
    'characters.Models.BaseModel',
    'characters.Models.bleachModels',
    'characters.Models.dbzModels',
    'characters.Models.genshinModels',
    'characters.Models.kofModels',
    'characters.Models.narutoModels',
    'characters.Models.oponenteModel',
    'core',
    'core.menu_log',
    'core.eventos',
    'core.sound',
    'core.mochila_log',
    'core.tienda_log',
    'asciimatics',
    'asciimatics.screen',
    'asciimatics.scene',
    'asciimatics.effects',
    'asciimatics.renderers',
    'ui',
    'ui.menu_ui',
    'ui.mochila_ui',
    'ui.tienda_ui',
    'ui.sprites',
    'ui.animations',
    'utils',
    'utils.colors',
    'utils.common',
    'utils.console',
    'utils.constants',
    'utils.data',
    'utils.errors',
]

a = Analysis(
    ['main.py'],
    pathex=['.', 'TerminalGameClient/src'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'PyQt6', 'PySide6'],
    noarchive=False,
    optimize=1,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='RPGTerminal',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon='assets/hub/Media-Hub.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='RPGTerminal',
)
