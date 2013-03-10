#!/usr/bin/env bash

set -e

APP_DIR="${STACKATO_DOCUMENT_ROOT}"
OUT_DIR="${APP_DIR}/build-root"
[ -d "${OUT_DIR}" ] || mkdir -p "${OUT_DIR}"
[ -d "${OUT_DIR}/dummy" ] || mkdir -p "${OUT_DIR}/dummy"

TARGET_FOLDER="STACKATO_FILESYSTEM_DXR_${DXR_TREE^^}_WWW"
cat >"${OUT_DIR}/dxr.config" <<-EOF

[DXR]
target_folder       = ${!TARGET_FOLDER}
nb_jobs             = 2
temp_folder         = ${OUT_DIR}/temp
log_folder          = ${OUT_DIR}/logs
enabled_plugins     = pygmentize clang
generated_date      = ${DATE}
template            = ${APP_DIR}/dxr/dxr/templates
plugin_folder       = ${APP_DIR}/dxr/dxr/plugins

[dxr]
source_folder       = ${APP_DIR}/dxr
build_command       = /usr/bin/env true
object_folder       = ${OUT_DIR}/dummy

[Template]
footer_text         =

EOF

dxr-build.py -f "${OUT_DIR}/dxr.config"
echo Done.

#  Prevent stackato from restarting this
while [ "$1" == "--hang" ] ; do
    sleep 3650d
done
