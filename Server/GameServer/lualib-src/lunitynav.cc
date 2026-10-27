// Portable Lua binding to the existing clean-room PathLib/CysNavMesh reader.
// The old grid-only map reader cannot parse the published triangle .path images.
#include "CysNavMesh.h"
#include <cmath>
#include <vector>
extern "C" {
#include "lua.h"
#include "lauxlib.h"
}
static const char* META="dragon_unity_nav";
static cys::NavMesh* self(lua_State* L){auto p=(cys::NavMesh**)luaL_checkudata(L,1,META);luaL_argcheck(L,*p!=nullptr,1,"closed navmesh");return *p;}
static cys::NavPoint point(lua_State* L,int index){
    luaL_checktype(L,index,LUA_TTABLE);lua_getfield(L,index,"x");double x=luaL_checknumber(L,-1);lua_pop(L,1);lua_getfield(L,index,"y");double z=luaL_checknumber(L,-1);lua_pop(L,1);
    luaL_argcheck(L,std::isfinite(x)&&std::isfinite(z)&&std::fabs(x)<1e7&&std::fabs(z)<1e7,index,"invalid nav coordinate");return {(float)x,(float)z};
}
static int create(lua_State* L){auto p=(cys::NavMesh**)lua_newuserdata(L,sizeof(cys::NavMesh*));*p=new cys::NavMesh();luaL_setmetatable(L,META);return 1;}
static int close(lua_State* L){auto p=(cys::NavMesh**)luaL_checkudata(L,1,META);delete *p;*p=nullptr;return 0;}
static int load(lua_State* L){auto nav=self(L);bool ok=nav->LoadFromFile(luaL_checkstring(L,2));ok=ok&&nav->Stats().points>=3&&nav->Stats().tris>0;if(!ok)nav->Unload();lua_pushboolean(L,ok);return 1;}
static int walkable(lua_State* L){auto nav=self(L);auto p=point(L,2);lua_pushboolean(L,nav->IsWalkable(p.x,p.z));return 1;}
static int visible(lua_State* L){auto nav=self(L);auto a=point(L,2),b=point(L,3);lua_pushboolean(L,nav->LineOfSight(a,b));return 1;}
static void push(lua_State* L,const cys::NavPoint& p){lua_newtable(L);lua_pushnumber(L,p.x);lua_setfield(L,-2,"x");lua_pushnumber(L,p.z);lua_setfield(L,-2,"y");}
static int findpath(lua_State* L){auto nav=self(L);auto a=point(L,2),b=point(L,3);std::vector<cys::NavPoint> points;nav->FindPath(a,b,points);lua_newtable(L);int index=1;for(const auto& p:points){push(L,p);lua_rawseti(L,-2,index++);}return 1;}
static int empty(lua_State* L){auto nav=self(L);auto p=point(L,2);if(nav->IsWalkable(p.x,p.z)){push(L,p);return 1;}
    for(int radius=1;radius<=8;++radius)for(int x=-radius;x<=radius;++x)for(int z=-radius;z<=radius;++z){
        if(std::abs(x)!=radius&&std::abs(z)!=radius)continue;cys::NavPoint candidate={p.x+x*.5f,p.z+z*.5f};if(nav->IsWalkable(candidate.x,candidate.z)){push(L,candidate);return 1;}}
    lua_pushnil(L);return 1;
}
extern "C" int luaopen_unitynav(lua_State* L){
    luaL_newmetatable(L,META);luaL_Reg methods[]={{"__gc",close},{"load",load},{"walkable",walkable},{"lineofsight",visible},{"findpath",findpath},{"findempty",empty},{nullptr,nullptr}};luaL_setfuncs(L,methods,0);lua_pushvalue(L,-1);lua_setfield(L,-2,"__index");lua_pop(L,1);
    luaL_Reg functions[]={{"new",create},{nullptr,nullptr}};luaL_newlib(L,functions);return 1;
}
