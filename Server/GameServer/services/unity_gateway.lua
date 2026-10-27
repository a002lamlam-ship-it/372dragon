-- Development transport for a new Unity client, with a basic server-owned PvE adapter.
local skynet = require 'skynet'
local socket = require 'skynet.socket'
local driver = require 'skynet.socketdriver'
local json = require 'cjson'
require 'skynet.manager'
local MAX_LINE = 65536
local combat
local function response(request,connection)
    if type(request) ~= 'table' or request == json.null then
        return {v=1, ok=false, error={code='INVALID_REQUEST'}}
    end
    local id = request.id
    if type(id) ~= 'string' or #id > 64 or id == '' then
        return {v=1, ok=false, error={code='INVALID_ID'}}
    end
    local reply = {v=1, id=id, ok=false}
    if request.v ~= 1 then
        reply.error = {code='UNSUPPORTED_VERSION'}
    elseif request.method == 'hello' then
        reply.ok = true
        reply.result = {protocol='372dragon.unity', version=1,
                        capabilities={'hello', 'ping', 'world.list', 'world.enter', 'world.entities', 'combat.join', 'combat.move', 'combat.attack', 'combat.snapshot', 'combat.respawn', 'combat.leave'}, gameplayReady=false, basicCombatAvailable=true, fullLegacySkills=false}
    elseif request.method == 'ping' then
        reply.ok = true
        reply.result = {pong=true}
    elseif request.method == 'world.list' or request.method == 'world.enter' or request.method == 'world.entities' then
        local result, code = require('unity_world').call(request.method, request.params)
        if result then reply.ok = true; reply.result = result else reply.error = {code=code} end
    elseif type(request.method)=='string' and request.method:match('^combat%.') then
        local result,code=combat:call(connection,request.method,request.params)
        if result then reply.ok=true;reply.result=result else reply.error={code=code}end
    else
        reply.error = {code='METHOD_NOT_IMPLEMENTED'}
    end
    return reply
end
skynet.start(function()
    assert(require('license_check').check_or_abort(), 'Gateway requires skip_license_check=true')
    combat=require('unity_combat').new(require('unity_world'))
    skynet.fork(function()while true do skynet.sleep(10);combat:tick()end end)
    local host = skynet.getenv('unity_host') or '127.0.0.1'
    local port = tonumber(skynet.getenv('unity_port') or '15800')
    local listener = socket.listen(host, port)
    socket.start(listener, function(fd)
        local ok, err = pcall(function()
            socket.start(fd)
            socket.limit(fd, MAX_LINE)
            while true do
                local line = socket.readline(fd, '\n')
                if not line then break end
                if #line > MAX_LINE then break end
                local decoded, request = pcall(json.decode, line)
                local reply = decoded and response(request,fd) or
                    {v=1, ok=false, error={code='INVALID_JSON'}}
                socket.write(fd, json.encode(reply)..'\n')
            end
        end)
        if not ok then skynet.error('Unity connection closed: '..tostring(err)) end
        combat:disconnect(fd)
        socket.close(fd)
    end)
    for _, info in pairs(driver.info()) do
        if info.id == listener then
            local actual = assert(info.sock:match(':(%d+)$'))
            io.stdout:write('UNITY_GATEWAY_READY '..actual..'\n')
            io.stdout:flush()
        end
    end
end)
