#!/usr/bin/env python

"""
DXR indexer wrapper to use the correct sqlite3 library
"""

import os
import sys
import time
from os import environ
from os.path import expanduser, exists, join

build_root = expanduser("~/build-root")
if not exists(join(build_root, "dummy")):
    os.makedirs(join(build_root, "dummy"))

target_folder = "STACKATO_FILESYSTEM_DXR_%s_WWW" % environ["DXR_TREE"].upper()
with open(join(build_root, "dxr.config"), "w") as config_file:
    config = """
    [DXR]
    target_folder       = {TARGET_FOLDER}
    nb_jobs             = 2
    temp_folder         = ${OUT_DIR}/temp
    log_folder          = ${OUT_DIR}/logs
    enabled_plugins     = pygmentize clang
    generated_date      = ${DATE}
    template            = ${HOME}/dxr/dxr/templates
    plugin_folder       = ${HOME}/dxr/dxr/plugins
    
    [dxr]
    source_folder       = ${HOME}/dxr
    build_command       = /usr/bin/env true
    object_folder       = ${OUT_DIR}/dummy
    
    [Template]
    footer_text         =
    """.format(TARGET_FOLDER=target_folder,
               OUT_DIR=os.environ["HOME"],
               DATE=os.environ.get("DATE", time.asctime()))
    for line in config.splitlines():
        config_file.write(line.lstrip())

import pysqlite2.dbapi2
sys.modules['sqlite3'] = pysqlite2.dbapi2

from dxr.build import build_instance
build_instance(join(build_root, "dxr.config"),
               nb_jobs=None,
               tree=None,
               verbose=False)

if "--hang" in sys.argv:
    while True:
        time.sleep(60 * 60 * 24 * 365 * 10)
