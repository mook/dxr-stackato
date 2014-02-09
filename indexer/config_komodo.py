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
        upstream_url = "https://github.com/Komodo/KomodoEdit.git"
        cache_key = ("STACKATO_FILESYSTEM_%s_CACHE" %
                     (os.environ.get("STACKATO_APP_NAME_UPCASE", "KOMODO"),))
        if cache_key in os.environ:
            cache_dir = join(os.environ[cache_key], "komodo")
            if exists(cache_dir):
                call(["git", "pull"], cwd=cache_dir)
            else:
                call(["git", "clone", "--bare", upstream_url, cache_dir])
            call(["git", "clone", cache_dir, komodo_dir])
            call(["git", "remote", "set-url", "origin", upstream_url], cwd=komodo_dir)
        else:
            call(["git", "clone", upstream_url, komodo_dir])

    config.set("komodo", "source_folder", komodo_dir)
    config.set("komodo", "ignore_patterns", " ".join([
        ".hg", ".git", ".svn", ".bzr", ".deps", ".libs", "*.pyc",
        "/mozilla/build", "/build/",
        "/src/codeintel/test2/scan_actual",
        "/src/codeintel/test2/scan_inputs/unicode/",
        "/src/codeintel/test2/tmp*"]))
    config.set("komodo", "enabled_plugins", "pygmentize omniglot urllink buglink")
    config.set("komodo", "plugin_buglink_name", "ActiveState Bugzilla")
    config.set("komodo", "plugin_buglink_url", "http://bugs.activestate.com/show_bug.cgi?id=%s")
