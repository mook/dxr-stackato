#!/usr/bin/env python

"""
DXR indexer wrapper to use the correct sqlite3 library
"""

import ConfigParser
import logging
import imp
import os
import shutil
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

class Config(ConfigParser.RawConfigParser):
    def set(self, section, option, value):
        try:
            self.add_section(section)
        except ConfigParser.DuplicateSectionError:
            pass
        ConfigParser.RawConfigParser.set(self, section, option, value)


# Initialize with default configuration
config = Config()
config.set("DXR", "target_folder", join(build_root, "www"))
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
        dist_path = environ["STACKATO_FILESYSTEM_DXR_WWW"]
        trees_path = join(dist_path, "trees")
        if not exists(trees_path):
            os.makedirs(trees_path, 0775)
        # Move the whole tree over first so it's on the same FS
        stage_path = join(trees_path, dxr_tree + ".stage")
        if exists(stage_path):
            shutil.rmtree(stage_path)
        shutil.move(join(build_root, "www", "trees", dxr_tree), stage_path)
        try:
            os.rename(join(trees_path, dxr_tree), join(trees_path, dxr_tree + ".old"))
        except:
            pass
        os.rename(stage_path, join(trees_path, dxr_tree))
        try:
            shutil.rmtree(join(trees_path, dxr_tree + ".old"))
        except:
            pass
        # Check if we actually have the correct folder structure set up...
        for dirpath, dirs, files in os.walk(join(build_root, "www")):
            for d in dirs:
                src_path = join(dirpath, d)
                dest_path = join(dist_path,
                                 os.path.relpath(src_path, join(build_root, "www")))
                if not exists(dest_path):
                    os.makedirs(dest_path, 0775)
            for f in files:
                src_path = join(dirpath, f)
                dest_path = join(dist_path,
                                 os.path.relpath(src_path, join(build_root, "www")))
                if not exists(dest_path):
                    shutil.move(src_path, dest_path)

        # Update the config if it doesn't know about our tree
        mod = imp.load_source("dxr_www_config", join(dist_path, "config.py"))
        if dxr_tree not in mod.TREES:
            mode.TREES[dxr_tree] = dxr_tree.title()
            config = """
            # Settings, filled out by dxr-build.py -f FILE

            from ordereddict import OrderedDict

            TREES                 = {TREES}
            WWW_ROOT              = {WWW_ROOT}
            GENERATED_DATE        = {GENERATED_DATE}
            DIRECTORY_INDEX       = {DIRECTORY_INDEX}
            """.format(TREES=repr(mod.TREES),
                       WWW_ROOT=repr(mod.WWW_ROOT),
                       GENERATED_DATE=repr(mod.GENERATED_DATE),
                       DIRECTORY_INDEX=repr(mod.DIRECTORY_INDEX))
            config = "\n".join(x.lstrip() for x in config.splitlines())
            with open(join(dist_path, "config.py"), "w") as config_file:
                config_file.write(config)
            try:
                os.remove(join(dist_path, "config.pyc"))
            except:
                pass # no precompiled cache?

if "--hang" in sys.argv:
    while True:
        time.sleep(60 * 60 * 24 * 365 * 10)
