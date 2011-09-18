# -*- coding: utf-8 -*-
#
# Created:    2010/10/13
# Author:         alisue
#
COMPRESS_CSS = {}
COMPRESS_JS = {}

#
# 動的に`compress_settings`内のPythonファイルを読み込みロードして
# `COMPRESS_CSS`と`COMPRESS_JS`を更新する
#
def load():
    import os, imp, glob
    root = os.path.dirname(__file__)
    for path in glob.glob("%s/*.py" % root):
        filename = os.path.basename(path)
        if filename == '__init__.py': continue
        mod = imp.load_source(filename, path)
        COMPRESS_CSS.update(mod.COMPRESS_CSS)
        COMPRESS_JS.update(mod.COMPRESS_JS)
load()