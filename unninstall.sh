#!/bin/sh -x

source ./common.sh

echo '${CAVEN_GUARD_START}'
COMMAND_SED="/${CAVEN_GUARD_START}/,/${CAVEN_GUARD_END}/{/${CAVEN_GUARD_START}/!{/${CAVEN_GUARD_END}/!d}}"
sed $COMMAND_SED ${BASH_RC_FILE} >> ./modified_caven_rc_manip
rm ${BASH_RC_FILE}
mv ./modified_caven_rc_manip ${BASH_RC_FILE}

rm -rf ${CAVEN_DIR}
