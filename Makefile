#directories
INC_DIR:=include
SRC_DIR:=src
TEST_DIR:=test
EXEC_DIR:=executables
BUILD_DIR:=./build

PROJ_NAME:=$(shell basename $(CURDIR))
SHARE_DIR:=$(BUILD_DIR)/$(PROJ_NAME)$(VERSION)
SHARE_INCLUDE_DIR:=$(SHARE_DIR)/$(INC_DIR)
SHARE_LIB:=$(SHARE_DIR)/lib/lib$(PROJ_NAME).a

HIDEN_HEADERS_DIR:=$(INC_DIR)/hide
OBJT_DIR:=$(BUILD_DIR)/objects
TEST_BUILD_DIR:=$(BUILD_DIR)/$(TEST_DIR)

DEPS_NAMES = $(shell for dep in $(DEPS); do echo $$dep | sed 's/.*\///' ; done)
DEPS_DIR = $(SHARE_DIR)/dependencies

#files
SRCS:=$(shell find $(SRC_DIR) -name "*.cpp")
OBJTS:=$(SRCS:$(SRC_DIR)/%.cpp=$(OBJT_DIR)/%.o) 
OBJTS_DEPS := $(OBJS:.o=.d)
PUBLIC_HEADERS= $(shell find $(INC_DIR) -not -path "$(HIDEN_HEADERS_DIR)/*" -type f)
SHARED_HEADERS= $(PUBLIC_HEADERS:$(INC_DIR)/%=$(SHARE_INCLUDE_DIR)/%)
TEST_SRCS=$(shell find $(TEST_DIR) -name "*.cpp")
TEST_TARGETS=$(TEST_SRCS:$(TEST_DIR)/%.cpp=$(TEST_BUILD_DIR)/%)

#flags
SHARE_INC_FLAGS = $(addprefix -I,$(shell find $(SHARE_DIR) -wholename "*/$(INC_DIR)" -type d))
INTERNAL_INC_FLAGS = -I$(INC_DIR) $(addprefix -I,$(shell find $(DEPS_DIR) -name "$(INC_DIR)" -type d))
LIB_FLAGS = -L$(dir $(SHARE_LIB)) -l$(PROJ_NAME)
LIB_FLAGS += $(addprefix -L,$(shell find $(DEPS_DIR) -name "lib" -type d)) $(addprefix -l,$(DEPS_NAMES))

#Compile objects
$(OBJT_DIR)/%.o : $(SRC_DIR)/%.cpp $(DEPS_DIR)
	@mkdir -p $(dir $@)
	g++ $(INTERNAL_INC_FLAGS) -MMD -MP -fPIC -c $< -o $@ $(LIB_FLAGS)
#Compile tests
$(TEST_BUILD_DIR)/% : $(TEST_DIR)/%.cpp $(SHARE_LIB)
	@mkdir -p $(dir $@)
	g++ $(INTERNAL_INC_FLAGS) $(OBJTS) $< -o $@ $(LIB_FLAGS)
#copy include files to build folder
$(SHARE_INCLUDE_DIR)/%: $(INC_DIR)/%
	@mkdir -p $(dir $@)
	@cp $< $@
#Create static library for project
$(SHARE_LIB): $(OBJTS)
	mkdir -p $(dir $@)
	ar -rc $@ $<


$(DEPS_DIR):
ifneq ($(DEPS),)
	@echo ----------------------------------------------------
	@echo Compiling Dependencies of project $(PROJ_NAME)
	@echo ----------------------------------------------------
	@echo
	@mkdir -p $(DEPS_DIR)
	@for dep in $(DEPS) ; 												\
		do DEP_NAME=$$( echo $$dep | sed 's/.*\///') ;  				\
		echo Compiling $$dep ... ;										\
		cd $$dep && $(MAKE) share && 									\
		cp -r $$dep/$(BUILD_DIR)/$$DEP_NAME $(CURDIR)/$(DEPS_DIR) &&  	\
		$(MAKE) clean ;													\
	done
else
	@echo $(PROJ_NAME) has no dependencies
endif

print:
	@echo $(DEPS)
	@echo $(DEPS_NAMES)
	@echo $(LIB_FLAGS)

compile_dependencies: $(DEPS_DIR)
compile_objects: $(OBJTS)
compile_tests:   $(TEST_TARGETS)
compile_lib: $(SHARE_LIB)
share_headers: $(SHARED_HEADERS)
share: compile_dependencies share_headers compile_lib
	@echo Shared $(PROJ_NAME)
run_tests: compile_tests
	for test in $(TEST_TARGETS) ; do $$test ; done
clean:
	rm -rd build

-include $(OBJTS_DEPS)



