MODULE_NAME=$(shell basename $(CURDIR))
BUILD_DIR=build
INC_DIR=include
SRC_DIR=src
TEST_DIR=test
EXE_DIR=executable

PRIVATE_INC=hide #subfolder of include
ALL_OBJCTS=$(shell find ${OBJCT_DIR} -type f 2> /dev/null)
PUBLIC_INC=${BUILD_DIR}/${INC_DIR}
DEPS_PUBLIC_INC=$(addsuffix /${PUBLIC_INC}, ${DEPS})

OBJCT_DIR=${BUILD_DIR}/objts
SRCS=$(shell find ${SRC_DIR} -type f)
OBJTS=$(SRCS:$(SRC_DIR)/%.cpp=$(OBJCT_DIR)/$(MODULE_NAME)__%.o)

TEST_BUILD=${BUILD_DIR}/${TEST_DIR}
TEST_SRCS=${shell find ${TEST_DIR} -name *.cpp 2> /dev/null}
TEST_TARGETS=${TEST_SRCS:${TEST_DIR}/%.cpp=${TEST_BUILD}/%}

EXE_BUILD=${BUILD_DIR}/${EXE_DIR}
EXE_SRCS=${shell find ${EXE_DIR} -name *.cpp 2> /dev/null}
EXE_TARGETS=${EXE_SRCS:${EXE_DIR}/%.cpp=${EXE_BUILD}/%}

${OBJCT_DIR}/${MODULE_NAME}__%.o: ${SRC_DIR}/%.cpp
	@echo " -> Compiling $<"
	@mkdir -p ${@D}
	@g++ -fPIC -c -I ${INC_DIR} $(addprefix -I ,${DEPS_PUBLIC_INC}) $< -o $@

${TEST_BUILD}/%: ${TEST_DIR}/%.cpp
	@echo " -> Linking $<"
	@mkdir -p ${@D}
	@g++ -I ${INC_DIR} ${ALL_OBJCTS} $< -o $@

${EXE_BUILD}/%: ${EXE_DIR}/%.cpp
	@echo " -> Linking $<"
	@mkdir -p ${@D}
	@g++ -I ${PUBLIC_INC} ${ALL_OBJCTS} $< -o $@

compile_dependencies: 
	@mkdir -p ${OBJCT_DIR}/deps
	@for dep in ${DEPS} ; do                                                      \
	    cd $$dep && ${MAKE} -s compile ;                                          \
		cd ${CURDIR} ;												              \
		\cp -r $$( find $$dep/${OBJCT_DIR} -type f -name *.o) ${OBJCT_DIR}/deps ; \
	done

disp_dep_files:
	@echo ${DEP_FILES}

show:
	@mkdir -p ${PUBLIC_INC}/${MODULE_NAME} 
	@rm -rf ${PUBLIC_INC}/${MODULE_NAME}
	@\cp -r ${INC_DIR} ${PUBLIC_INC}/${MODULE_NAME}
	@rm -rf ${PUBLIC_INC}/${MODULE_NAME}/${PRIVATE_INC} 
show_all: 
	@for dep in ${DEPS} ; do cd $$dep && ${MAKE} show ; done

compile: compile_dependencies compile_fast

compile_fast:
	@echo "Compiling ${MODULE_NAME}..."
	@${MAKE} -s ${OBJTS} show

link_tests: compile ${TEST_TARGETS}
link_tests_fast: compile_fast ${TEST_TARGETS}

link_executables: compile ${EXE_TARGETS}
link_executables_fast: compile_fast ${EXE_TARGETS}

run_tests: link_tests do_run_tests
run_tests_fast: link_tests_fast do_run_tests

do_run_tests:
	@printf "\n     RUNNING TESTS      \n\n"
	@for test in ${TEST_TARGETS} ; do ./$$test ; done

all: link_tests link_executables

clean:
	@rm -rf build

clean_all: clean
	@for dep in ${DEPS} ; do cd $$dep && ${MAKE} -s clean_all ; done