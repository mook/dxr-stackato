#!/usr/bin/env python

"""
DXR indexer wrapper to use the correct sqlite3 library
"""

import logging
import os
import sys
import time
from os import environ
from os.path import expanduser, exists, join

logging.basicConfig(stream=sys.stdout)

build_root = expanduser("~/build-root")
if not exists(join(build_root, "dummy")):
    os.makedirs(join(build_root, "dummy"))

target_folder = environ["STACKATO_FILESYSTEM_DXR_%s_WWW" % environ["DXR_TREE"].upper()]
with open(join(build_root, "dxr.config"), "w") as config_file:
    config = """
    [DXR]
    target_folder       = {TARGET_FOLDER}
    nb_jobs             = 2
    temp_folder         = {BUILD_ROOT}/temp
    log_folder          = {BUILD_ROOT}/logs
    enabled_plugins     = pygmentize clang
    generated_date      = {DATE}
    template            = {HOME}/dxr/dxr/templates
    plugin_folder       = {HOME}/dxr/dxr/plugins
    
    [dxr]
    source_folder       = {HOME}/dxr
    build_command       = /usr/bin/env true
    object_folder       = {BUILD_ROOT}/dummy
    
    [Template]
    footer_text         =
    """.format(TARGET_FOLDER=target_folder,
               BUILD_ROOT=build_root,
               HOME=os.environ["HOME"],
               DATE=os.environ.get("DATE", time.asctime()))
    for line in config.splitlines():
        config_file.write(line.lstrip() + "\n")

import pysqlite2.dbapi2
sys.modules['sqlite3'] = pysqlite2.dbapi2

try:
    from dxr.build import build_instance
except ImportError:
    logging.root.exception("Failed to import")
else:
    try:
        build_instance(join(build_root, "dxr.config"),
                       nb_jobs=None,
                       tree=None,
                       verbose=False)
    except:
        logging.root.exception("Failed to build")

if "--hang" in sys.argv:
    while True:
        time.sleep(60 * 60 * 24 * 365 * 10)
