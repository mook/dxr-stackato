#!/bin/sh
echo "Running pre-staging hook..."
echo "Running pre-staging hook..." >&2
set -e
cd "${HOME}"
# Don't use alternates in the VM, they don't exist
rm -f .dxr/.git/objects/info/alternates
