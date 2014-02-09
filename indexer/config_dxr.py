"""Configuration for the DXR tree"""

import os.path

def make_config(config):
    """Update the DXR configuration file.
    @param config {ConfigParser.RawConfigParser} DXR configuration
    """
    config.set("dxr", "source_folder", os.path.expanduser("~/dxr"))
