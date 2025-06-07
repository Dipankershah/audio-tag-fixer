# -*- mode: python ; coding: utf-8 -*-
# Windows-specific PyInstaller spec file

a = Analysis(
    ['audio_tag_fixer.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'mutagen',
        'mutagen.id3',
        'mutagen.mp3', 
        'mutagen.flac',
        'mutagen.mp4',
        'mutagen.oggvorbis',
        'mutagen.asf',
        'mutagen._vorbis',
        'mutagen.apev2',
        'mutagen.id3._frames',
        'mutagen.id3._util',
        'mutagen._util',
        'mutagen.trueaudio',
        'mutagen.wavpack',
        'mutagen.musepack',
        'mutagen.monkeysaudio',
        'mutagen.optimfrog',
        'mutagen.aiff',
        'mutagen.dsf',
        'mutagen.wave',
        're'
    ],
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
    name='AudioTagFixer-Windows',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None
) 