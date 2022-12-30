# -*- mode: python -*-

from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path
import sys

app_name = 'KDHS Messenger'
sys.path += ["src\\"]

block_cipher = None

a = Analysis(['src\\main.py'],
  pathex=['E:\\KDHS-clone\\'],
  binaries=None,
  datas=None,

  hiddenimports=[
  'twisted.internet',
  'twisted.internet._threadedselect',
  'plyer',
  'plyer.platforms',
  'plyer.platforms.win',
  'plyer.platforms.win.notification',
  'plyer.facades',
  'plyer.facades.notification',
  '__init__',
  ],

  hookspath=[kivymd_hooks_path],
  runtime_hooks=[],
  excludes=[],
  win_no_prefer_redirects=False,
  win_private_assemblies=False,
  cipher=block_cipher)

# exclusion list
from os.path import join
from fnmatch import fnmatch
exclusion_patterns = (
  join("kivy_install", "data", "images", "testpattern.png"),
  join("kivy_install", "data", "images", "image-loading.gif"),
  join("kivy_install", "data", "keyboards*"),
  join("kivy_install", "data", "settings_kivy.json"),
  join("kivy_install", "data", "logo*"),
  join("kivy_install", "data", "fonts", "DejaVuSans*"),
  join("kivy_install", "modules*"),
  join("Include*"),
  join("sdl2-config"),

  # Filter app directory
  join(".idea*"),
  join("*.git"),
  join("*.gitignore"),
  join("test.py"),
  join("*.bat"),
  join("*.pickle"),
  join("*.txt"),
  join("*.log"),
  join("*.md"),
  join("__pycache__"),
  join("*.vs")
)
exclusion_patterns = ()
def can_exclude(fn):
    for pat in exclusion_patterns:
        if fnmatch(fn, pat):
            return True

a.datas = [x for x in a.datas if not can_exclude(x[0])]
a.binaries = [x for x in a.binaries if not can_exclude(x[0])]
# Filter app directory
appfolder = [x for x in Tree('src\\', excludes=[]) if not can_exclude(x[0])]  

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
  a.scripts,
  exclude_binaries=True,
  name=app_name,
  debug=False,
  strip=False,
  upx=True,
  console=False,
  icon="src\\assets\\icons\\app.ico")

coll = COLLECT(exe, appfolder,
  a.binaries,
  a.zipfiles,
  a.datas,
  *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins )],
  strip=False,
  upx=True,
  name=app_name)