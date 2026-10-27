-- Read-only exported placements, loaded lazily; not a legacy gameplay simulation.
local json = require 'cjson'
local skynet = require 'skynet'
local M = {}
local catalog, entries, worlds, order, root
local function load_json(path)
    local file=io.open(path,'rb')
    if not file then return nil end
    local raw=file:read('*a');file:close()
    local ok,value=pcall(json.decode,raw)
    if ok then return value end
end
local function initialize()
    if catalog then return end
    root=skynet.getenv('unity_world_root')
    catalog=root and load_json(root..'/catalog.json') or {schema=1,scenes={}}
    catalog=catalog or {schema=1,scenes={}}
    entries={};worlds={};order={}
    for _,info in ipairs(catalog.scenes) do entries[info.sceneId]=info end
end
local function pagination(params)
    local offset=params.offset or 0
    local limit=params.limit or 50
    if type(offset)~='number' or offset<0 or offset%1~=0 or type(limit)~='number' or limit<1 or limit>100 or limit%1~=0 then
        return nil,nil,'INVALID_PAGINATION'
    end
    return offset,limit
end
local function get_world(id)
    if not entries[id] then return nil end
    if worlds[id] then return worlds[id] end
    local world=load_json(root..'/'..string.format('%d',id)..'.json')
    if not world or world.schema~=1 then return nil end
    if #order>=4 then worlds[table.remove(order,1)]=nil end
    worlds[id]=world;order[#order+1]=id
    return world
end
function M.call(method,params)
    initialize()
    if method=='world.list' then
        if #catalog.scenes==0 then return nil,'WORLD_DATA_UNAVAILABLE' end
        if params~=nil and params~=json.null and type(params)~='table' then return nil,'INVALID_PARAMS' end
        local offset,limit,error=pagination(type(params)=='table' and params or {})
        if error then return nil,error end
        if offset>=#catalog.scenes then return nil,'PAGE_OUT_OF_RANGE' end
        local scenes={}
        for i=offset+1,math.min(offset+limit,#catalog.scenes) do scenes[#scenes+1]=catalog.scenes[i] end
        return {scenes=scenes,total=#catalog.scenes,nextOffset=math.min(offset+limit,#catalog.scenes),simulationReady=false}
    end
    if type(params)~='table' then return nil,'INVALID_PARAMS' end
    if type(params.sceneId)~='number' or params.sceneId%1~=0 then return nil,'WORLD_NOT_FOUND' end
    local world=get_world(params.sceneId)
    if not world then return nil,'WORLD_NOT_FOUND' end
    if method=='world.enter' then
        return {sceneId=world.sceneId,name=world.name,width=world.width,depth=world.depth,sceneType=world.sceneType,
            entityCount=#world.entities,simulationReady=false,coordinates=world.coordinates}
    end
    local offset,limit,error=pagination(params)
    if error then return nil,error end
    if offset>=#world.entities then return nil,'PAGE_OUT_OF_RANGE' end
    local items={}
    for i=offset+1,math.min(offset+limit,#world.entities) do items[#items+1]=world.entities[i] end
    return {sceneId=world.sceneId,items=items,total=#world.entities,nextOffset=math.min(offset+limit,#world.entities),simulationReady=false}
end
function M.get_world(id)
    initialize()
    return get_world(id)
end
function M.data_root()
    initialize()
    return root
end
return M
