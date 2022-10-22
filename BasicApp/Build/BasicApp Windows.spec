from kivy.deps import sdl2, glew
# -*- mode: python -*-

block_cipher = None

a = Analysis(['..\\main.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['ffpyplayer', 'numpy', 'PIL', 'cv2', 'scipy', 'docutils', 'kivy-deps.gstreamer', 'kivy_deps.gstreamer', 'gstplayer', 'cryptography'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Basic App',
          debug=False,
          strip=False,
          upx=True,
          console=True)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='Basic App')
