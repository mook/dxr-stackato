import os
import os.path

print(os.environ.get("LD_LIBRARY_PATH", "<missing>"))

ld_library_path = os.environ.get("LD_LIBRARY_PATH", "").split(os.pathsep)
ld_library_path.append(os.path.expanduser("~/dxr/trilite"))
os.environ["LD_LIBRARY_PATH"] = os.pathsep.join(filter(bool, ld_library_path))

os.execvp("dxr-serve.py", ["dxr-serve.py", "--all", "--threaded",
                           os.environ["DXR_FOLDER"]])
