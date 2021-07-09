source ./common.sh

CAVEN_MATERIALS_DIR=${CAVEN_DIR}/caven_materials
CAVEN_SCRIPTS_DIR=${CAVEN_MATERIALS_DIR}/scripts

#create folder for caven
mkdir -p ${CAVEN_DIR}
mkdir -p ${CAVEN_MATERIALS_DIR}
mkdir -p ${CAVEN_SCRIPTS_DIR}

#Copy files into it
cp ./create.sh ${CAVEN_SCRIPTS_DIR}
cp ./Makefile ${CAVEN_MATERIALS_DIR}/caven_make
cp ./default_makefile ${CAVEN_MATERIALS_DIR}/default_makefile

#line that denotes beginning of bashrc code
echo "" >> ${BASH_RC_FILE}
echo "#_CAVEN_START_" >> ${BASH_RC_FILE}
echo "CAVEN_DIR=${CAVEN_DIR}" >> ${BASH_RC_FILE}

echo "alias caven_create=\"source ${CAVEN_SCRIPTS_DIR}/create.sh\"" >> ${BASH_RC_FILE}

#line that denotes beginning of bashrc code
echo "#_CAVEN_END___" >> ${BASH_RC_FILE}

source ${BASH_RC_FILE}