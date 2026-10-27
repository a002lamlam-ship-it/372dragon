LUA_CLIB_PATH ?= luaclib
CSERVICE_PATH ?= cservice

SKYNET_INC = framework/skynet-src
LUA_INC = framework/3rd/lua
SHARED ?= -fPIC --shared
PROFILE_FLAGS ?= -DUSE_RDTSC
CFLAGS = -g -O0 -Wall
CXXFLAGS = -g -fpermissive -std=c++17
ifeq ($(shell uname -s),Darwin)
SHARED = -fPIC -bundle -Wl,-undefined,dynamic_lookup
CXXFLAGS = -g -std=c++17
PROFILE_FLAGS =
endif

BT_STATICLIB := 3rd/behaviortree_cpp/lib/libbehaviortree_cpp.a
BT_LIB ?= $(BT_STATICLIB)
BT_INC ?= 3rd/behaviortree_cpp/include
SOL2_INC  ?= lualib-src/sol/

NAV_MESH_SRC ?= lualib-src/navmesh/*.cpp
AI_SCRIPT_SRC ?= lualib-src/ai/*.cpp
PROFILE_SRC ?=lualib-src/profile/*.c
LFS_SRC ?=lualib-src/lfs/*.c
RAX_SRC ?=lualib-src/rax/*.c

LUA_CLIB = unitynav \
  netpack \
  gbk \
  map \
  ldump \
  lnavmesh \
  laiscript \
  lprofile \
  lfs \
  rax

CSERVICE = caoi

all : \
  $(foreach v, $(CSERVICE), $(CSERVICE_PATH)/$(v).so) \
  $(foreach v, $(LUA_CLIB), $(LUA_CLIB_PATH)/$(v).so) 

$(LUA_CLIB_PATH)/netpack.so : lualib-src/lua-netpack.c | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) -I$(LUA_INC) -I$(SKYNET_INC) $(SHARED) $^ -o $@

$(LUA_CLIB_PATH)/gbk.so : lualib-src/gbk/lgbk.c | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) -I$(LUA_INC) -I$(SKYNET_INC) $(SHARED) $^ -o $@

$(LUA_CLIB_PATH)/map.so : lualib-src/map/lmap.cc lualib-src/map/Map.cc lualib-src/map/PathFinder.cc | $(LUA_CLIB_PATH)
	$(CXX) $(CFLAGS) -I$(LUA_INC) -I$(SKYNET_INC) $(SHARED) $^ -o $@

$(LUA_CLIB_PATH)/ldump.so : lualib-src/ldump.c | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) -I$(LUA_INC) -I$(SKYNET_INC) $(SHARED) $^ -o $@

$(LUA_CLIB_PATH)/lbt.so : lualib-src/lbt.cc $(BT_LIB) | $(LUA_CLIB_PATH)
	$(CXX) $(CXXFLAGS) -I$(LUA_INC) -I$(SKYNET_INC) -I$(SOL2_INC) -I$(BT_INC) $(SHARED) $^ -o $@

$(LUA_CLIB_PATH)/lnavmesh.so : lualib-src/lnavmesh.cc $(NAV_MESH_SRC) | $(LUA_CLIB_PATH)
	$(CXX) $(CXXFLAGS) -I$(LUA_INC) -I$(SKYNET_INC) -I$(SOL2_INC) $(SHARED) $^ -o $@

$(LUA_CLIB_PATH)/laiscript.so : lualib-src/laiscript.cc $(AI_SCRIPT_SRC) | $(LUA_CLIB_PATH)
	$(CXX) $(CXXFLAGS) -I$(LUA_INC) -I$(SKYNET_INC) -I$(SOL2_INC) $(SHARED) $^ -o $@

$(LUA_CLIB_PATH)/lprofile.so : $(PROFILE_SRC) | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) -I$(LUA_INC) -I$(SKYNET_INC) $(SHARED) $(PROFILE_FLAGS) $^ -o $@

$(LUA_CLIB_PATH)/lfs.so : $(LFS_SRC) | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) -I$(LUA_INC) -I$(SKYNET_INC) $(SHARED) $^ -o $@

$(LUA_CLIB_PATH)/rax.so : $(RAX_SRC) | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) -I$(LUA_INC) -I$(SKYNET_INC) $(SHARED) $^ -o $@

$(LUA_CLIB_PATH) :
	mkdir -p $(LUA_CLIB_PATH)
$(CSERVICE_PATH) :
	mkdir -p $(CSERVICE_PATH)

define CSERVICE_TEMP
  $$(CSERVICE_PATH)/$(1).so : service-src/service_$(1).c | $$(CSERVICE_PATH)
	$$(CC) $$(CFLAGS) $$(SHARED) $$< -o $$@ -Iframework/skynet-src
endef

$(foreach v, $(CSERVICE), $(eval $(call CSERVICE_TEMP,$(v))))

clean :
	rm -f $(LUA_CLIB_PATH)/*.so



UNITY_NAV_SRC = lualib-src/lunitynav.cc ../../Src/Client/WXClient/World/CysNavMesh.cpp $(wildcard ../../Src/Engine/PathLib/*.cpp)
$(LUA_CLIB_PATH)/unitynav.so : $(UNITY_NAV_SRC) | $(LUA_CLIB_PATH)
	$(CXX) $(CXXFLAGS) $(SHARED) -I$(LUA_INC) -I../../Src/Engine/PathLib -I../../Src/Client/WXClient/World $^ -o $@
