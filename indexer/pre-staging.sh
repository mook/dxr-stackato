#!/usr/bin/env bash
set -e

# Grab the clang binaries from llvm.org; having issues with using the package
# from precise-updates/universe
wget -O "${TMPDIR:-/tmp}/clang.tar.xz" --quiet \
    "http://llvm.org/releases/3.4/clang+llvm-3.4-x86_64-unknown-ubuntu12.04.tar.xz"
[ -d "${HOME}/clang" ] || mkdir "${HOME}/clang"
tar xJf "${TMPDIR:-/tmp}/clang.tar.xz" -C "${HOME}/clang" \
    --strip-components=1 --checkpoint=1000 --checkpoint-action=dot
