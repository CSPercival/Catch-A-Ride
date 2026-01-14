# --- Global Configuration ---
CXX      := g++
CPPFLAGS := -MMD -MP 
INCLUDE_FLAGS := -I. 

CXXFLAGS_COMMON  := -std=c++23 -Wall -Wextra -Wshadow -Wconversion -Wfloat-equal $(INCLUDE_FLAGS)
CXXFLAGS_RELEASE := $(CXXFLAGS_COMMON) -O3
CXXFLAGS_DEBUG   := $(CXXFLAGS_COMMON) -O0 -g -fsanitize=address,undefined

MODE ?= release
ifeq ($(MODE),release)
    CXXFLAGS := $(CXXFLAGS_RELEASE)
    LDFLAGS  := 
else ifeq ($(MODE),debug)
    CXXFLAGS := $(CXXFLAGS_DEBUG)
    LDFLAGS  := -fsanitize=address,undefined
else
    $(error Unknown MODE '$(MODE)'; use 'debug' or 'release')
endif

# --- Target 1: Transit Engine ---
TE_TARGET   := transit_engine
TE_SRC_DIRS := . shared_structs transit_matrix_preprocess
TE_OBJ_DIR  := obj-transit_engine
TE_SRCS     := $(shell find $(TE_SRC_DIRS) -maxdepth 1 -name "*.cpp")
TE_OBJS     := $(TE_SRCS:%.cpp=$(TE_OBJ_DIR)/%.o)
TE_DEPS     := $(TE_OBJS:.o=.d)

# --- Target 2: Ingestor ---
IN_TARGET   := ingestor
IN_SRC_DIRS := . shared_structs data_ingestor
IN_OBJ_DIR  := obj-ingestor
IN_SRCS     := $(shell find $(IN_SRC_DIRS) -maxdepth 1 -name "*.cpp")
IN_OBJS     := $(IN_SRCS:%.cpp=$(IN_OBJ_DIR)/%.o)
IN_DEPS     := $(IN_OBJS:.o=.d)

# --- Rules ---

all: $(TE_TARGET) $(IN_TARGET)

# Link Transit Engine
$(TE_TARGET): $(TE_OBJS)
	$(CXX) $(TE_OBJS) $(LDFLAGS) -o $@

# Link Ingestor
$(IN_TARGET): $(IN_OBJS)
	$(CXX) $(IN_OBJS) $(LDFLAGS) -o $@

# Compile Pattern for Transit Engine
$(TE_OBJ_DIR)/%.o: %.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $< -o $@

# Compile Pattern for Ingestor
$(IN_OBJ_DIR)/%.o: %.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $< -o $@

clean:
	rm -rf $(TE_OBJ_DIR) $(IN_OBJ_DIR) $(TE_TARGET) $(IN_TARGET)

# Include all dependency files
-include $(TE_DEPS) $(IN_DEPS)

.PHONY: all clean