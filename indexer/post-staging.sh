#!/bin/sh
set -e
echo "Running post-staging hook" >&2
export LLVM_CONFIG=llvm-config-3.3
export PLUGINS="pygmentize urllink omniglot"
make -C dxr
( cd dxr && {
    python setup.py build # --debug
    python setup.py install --user --skip-build
})
cp -f sqlite3.py ${PYTHONUSERBASE}/lib/python2.7/site-packages
