#!/bin/sh
set -e
echo "Running post-staging hook" >&2
export PATH="${HOME}/clang/bin:${PATH}"
cp -f sqlite3.py ${PYTHONUSERBASE}/lib/python2.7/site-packages
make -C dxr
( cd dxr && {
    python setup.py build # --debug
    python setup.py install --user --skip-build
})
