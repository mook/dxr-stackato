#!/bin/sh
set -e
make -C dxr PLUGINS=
PY_VER=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo $PYTHONUSERBASE/lib/python${PY_VER}
mkdir -p $PYTHONUSERBASE/lib/python${PY_VER}
cp -f sqlite3.py $PYTHONUSERBASE/lib/python${PY_VER}/site-packages/
cd dxr
    python setup.py build --debug
    python setup.py install --user --skip-build
