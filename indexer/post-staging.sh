#!/bin/sh
set -e
echo "Running post-staging hook" >&2
        #- "[ ! -d /staging/staged/python/bin/ ] && mkdir -p /staging/staged/python/bin/"
    
#- ln -s `which clang-3.2` /staging/staged/python/bin/clang
#- ln -s `which clang++-3.2` /staging/staged/python/bin/clang++
#- ln -s `which llvm-config-3.2` /staging/staged/python/bin/llvm-config
cp -f sqlite3.py ${PYTHONUSERBASE}/lib/python2.7/site-packages
make -C dxr
( cd dxr && {
    python setup.py build # --debug
    python setup.py install --user --skip-build
})
