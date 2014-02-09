import ctypes
import os
import os.path

# Fake out the path to libtrilite.so
old_CDLL = ctypes.CDLL
def replacement_CDLL(name, mode=ctypes.DEFAULT_MODE, handle=None, use_errno=False, use_last_error=False):
    if name == "libtrilite.so":
        name = os.path.expanduser("~/dxr/trilite/libtrilite.so")
    return old_CDLL(name, mode, handle, use_errno, use_last_error)
ctypes.CDLL = replacement_CDLL

try:
    from dxr.app import make_app

    app = make_app(os.path.abspath(os.environ["DXR_FOLDER"]))
    app.debug = True
    app.run(host=os.environ["VCAP_APP_HOST"],
            port=int(os.environ["VCAP_APP_PORT"]),
            processes=1,
            threaded=False)
except Exception as ex:
    import logging
    import sys
    logging.basicConfig(stream=sys.stdout)
    logging.root.exception(ex)

    # Fall back to avoid begin killed by Stackato
    from flask import Flask
    app = Flask("DXR-server-fallback",
                instance_path=os.path.abspath(os.environ["DXR_FOLDER"]))
    @app.route("/")
    def dummy():
        return "Application failed to start: %s" % (ex,)
    app.debug = True
    app.run(host=os.environ["VCAP_APP_HOST"],
            port=int(os.environ["VCAP_APP_PORT"]),
            processes=1,
            threaded=False)
