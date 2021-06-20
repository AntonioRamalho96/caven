#directories
INC_DIR:=include
SRC_DIR:=src
TEST_DIR:=test
EXEC_DIR:=executables
BUILD_DIR:=./build
PROJ_NAME:=$(shell basename $(CURDIR))

SHARE_DIR:=$(BUILD_DIR)/$(PROJ_NAME)$(VERSION)
SHARE_INCLUDE_DIR:=$(SHARE_DIR)/$(INC_DIR)
SHARE_LIB:=$(SHARE_DIR)/lib$(PROJ_NAME).a

HIDEN_HEADERS_DIR:=$(INC_DIR)/hide
OBJT_DIR:=$(BUILD_DIR)/objects
TEST_BUILD_DIR:=$(BUILD_DIR)/$(TEST_DIR)

#files
SRCS:=$(shell find $(SRC_DIR) -name "*.cpp")
OBJTS:=$(SRCS:$(SRC_DIR)/%.cpp=$(OBJT_DIR)/%.o) 
DEPS := $(OBJS:.o=.d)
PUBLIC_HEADERS= $(shell find $(INC_DIR) -not -path "$(HIDEN_HEADERS_DIR)/*" -type f)
SHARED_HEADERS= $(PUBLIC_HEADERS:$(INC_DIR)/%=$(SHARE_INCLUDE_DIR)/%)
TEST_SRCS=$(shell find $(TEST_DIR) -name "*.cpp")
TEST_TARGETS=$(TEST_SRCS:$(TEST_DIR)/%.cpp=$(TEST_BUILD_DIR)/%)

#flags
SHARE_INC_FLAGS = $(addprefix -I,$(shell find $(SHARE_DIR) -wholename "*/$(INC_DIR)" -type d))
INTERNAL_INC_FLAGS = -I$(INC_DIR)
LIB_FLAGS = -L$(dir $(SHARE_LIB)) -l$(PROJ_NAME)

#share include files
$(SHARE_INCLUDE_DIR)/%: $(INC_DIR)/%
	@mkdir -p $(dir $@)
	@cp $< $@

$(OBJT_DIR)/%.o : $(SRC_DIR)/%.cpp
	@mkdir -p $(dir $@)
	g++ $(INTERNAL_INC_FLAGS) -MMD -MP -fPIC -c $< -o $@

$(SHARE_LIB): $(OBJTS)
	mkdir -p $(dir $@)
	ar -rc $@ $<

$(TEST_BUILD_DIR)/% : $(TEST_DIR)/%.cpp $(SHARE_LIB)
	@mkdir -p $(dir $@)
	g++ $(INTERNAL_INC_FLAGS) $(OBJTS) $< -o $@ $(LIB_FLAGS)

print:
	@echo $(SHARE_LIB)

compile_objects: $(OBJTS)
compile_tests:   $(TEST_TARGETS)
compile_lib: $(SHARE_LIB)
share_headers: $(SHARED_HEADERS)
share: share_headers compile_lib
run_tests: compile_tests
	for test in $(TEST_TARGETS) ; do $$test ; done
clean:
	rm -rd build

-include $(DEPS)



