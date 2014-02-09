#!/usr/bin/env python

import os

from os.path import exists, join
from subprocess import check_call as call

def make_config(config):
    """Update the DXR configuration file.
    @param config {ConfigParser.RawConfigParser} DXR configuration
    """

    build_root = os.path.expanduser("~/build-root")
    komodo_dir = join(build_root, "komodo")

    if not exists(build_root):
        os.makedirs(build_root)

    if exists(komodo_dir):
        call(["git", "pull"], cwd=komodo_dir)
    else:
        call(["git", "clone", "https://github.com/Komodo/KomodoEdit.git", komodo_dir])
    config.set("komodo", "source_folder", komodo_dir)
    config.set("komodo", "ignore_patterns", " ".join([
        ".hg", ".git", ".svn", ".bzr", ".deps", ".libs", "*.pyc",
        "/mozilla/build", "/build/",
        "/src/codeintel/test2/scan_actual",
        "/src/codeintel/test2/scan_inputs/unicode/",
        "/src/codeintel/test2/tmp*"]))
