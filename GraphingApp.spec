# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['GraphingApp.py'],
    pathex=[],
    binaries=[],
    datas=[('base_background.png', '.'), ('white.png', '.'), ('blue.png', '.'), ('Gamma.jpg', '.')],
    hiddenimports=['matplotlib.backends.backend_pdf'],
    hookspath=[],
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
    a.binaries,
    a.datas,
    [],
    name='GraphingApp',
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
    icon=['Gamma.jpg'],
)
