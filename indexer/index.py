#!/usr/bin/env python

"""
DXR indexer wrapper to use the correct sqlite3 library
"""

import ConfigParser
import logging
import imp
import os
import sys
import time
from os import environ
from os.path import expanduser, exists, join

logging.basicConfig(stream=sys.stdout)
log = logging.getLogger("launcher")
log.setLevel(logging.DEBUG)

build_root = expanduser("~/build-root")
if not exists(join(build_root, "dummy")):
    os.makedirs(join(build_root, "dummy"))

dxr_tree = environ["DXR_TREE"]
target_folder = environ["STACKATO_FILESYSTEM_DXR_%s_WWW" % dxr_tree.upper()]

class Config(ConfigParser.RawConfigParser):
    def set(self, section, option, value):
        try:
            self.add_section(section)
        except ConfigParser.DuplicateSectionError:
            pass
        ConfigParser.RawConfigParser.set(self, section, option, value)


# Initialize with default configuration
config = Config()
config.set("DXR", "target_folder", target_folder)
config.set("DXR", "nb_jobs", "2")
config.set("DXR", "temp_folder", join(build_root, "temp"))
config.set("DXR", "log_folder", join(build_root, "logs"))
config.set("DXR", "enabled_plugins", os.environ.get("PLUGINS", "pygmentize"))
config.set("DXR", "generated_date", os.environ.get("DATE", time.asctime()))
config.set("DXR", "template", expanduser("~/dxr/dxr/templates"))
config.set("DXR", "plugin_folder", expanduser("~/dxr/dxr/plugins"))
config.set(dxr_tree, "build_command", "/usr/bin/env true $jobs")
config.set(dxr_tree, "object_folder", join(build_root, "dummy"))
config.set("Template", "footer_text", "")

# Load tree-specific overrides
try:
    mod_info = imp.find_module("config_%s" % (dxr_tree,), [os.environ["HOME"]])
except ImportError:
    log.warn("Could not find prep file %s",
             os.path.expanduser("~/config_%s.py" % (dxr_tree,)))
else:
    try:
        mod = imp.load_module("config_%s" % (dxr_tree,), *mod_info)
        mod.make_config(config)
    finally:
        if mod_info[0] is not None:
            mod_info[0].close()

# write configurate to disk
with open(join(build_root, "dxr.config"), "w") as config_file:
    config.write(config_file)

import pysqlite2.dbapi2
sys.modules['sqlite3'] = pysqlite2.dbapi2

try:
    from dxr.build import build_instance
except ImportError:
    log.exception("Failed to import")
else:
    try:
        build_instance(join(build_root, "dxr.config"),
                       nb_jobs=None,
                       tree=None,
                       verbose=False)
    except:
        log.exception("Failed to build")
    else:
        # TODO: Move files to target folder
        pass

if "--hang" in sys.argv:
    while True:
        time.sleep(60 * 60 * 24 * 365 * 10)
