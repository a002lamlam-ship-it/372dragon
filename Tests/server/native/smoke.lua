local skynet = require 'skynet'
local socket = require 'skynet.socket'
require 'skynet.manager'
skynet.start(function()
    local ok, err = xpcall(function()
        assert(require('license_check').check_or_abort(), 'development startup without llicense')
        for _, name in ipairs({'unitynav', 'gbk', 'map', 'ldump', 'lnavmesh', 'laiscript', 'lfs', 'rax', 'lprofile.c', 'lcipher.c', 'ltls.c', 'bson', 'md5', 'pb', 'sproto', 'lpeg', 'cjson', 'zlib', 'skiplist.c', 'textfilter', 'luarsa'}) do
            assert(require(name), name)
        end
        local gbk = require 'gbk'
        assert(gbk.fromutf8(gbk.toutf8('native-test')) == 'native-test')
        local nav = require 'lnavmesh'
        local point = nav.Point.new(1, 2, 0)
        assert(point.x == 100 and point.y == 200)
        local received = false
        local listener = socket.listen('127.0.0.1', 0)
        socket.start(listener, function(id)
            socket.start(id)
            assert(socket.read(id, 4) == 'ping')
            socket.write(id, 'pong')
            received = true
            socket.close(id)
        end)
        local info = require('skynet.socketdriver').info()
        local port
        for _, s in pairs(info) do
            if s.id == listener then port = tonumber(s.sock:match(':(%d+)$')) end
        end
        assert(port, 'listener port')
        local client = assert(socket.open('127.0.0.1', port))
        socket.write(client, 'ping')
        assert(socket.read(client, 4) == 'pong')
        assert(received)
        socket.close(client)
        socket.close(listener)
        local profiler = require 'lprofile.c'
        profiler.start()
        local sum = 0
        for i = 1, 1000 do sum = sum + i end
        assert(sum == 500500)
        local elapsed = profiler.dump()
        profiler.stop()
        assert(type(elapsed) == 'number' and elapsed >= 0 and elapsed < 10000000, 'profiler clock')
        local before = skynet.now()
        skynet.sleep(2)
        assert(skynet.now() > before, 'timer must advance')
    end, debug.traceback)
    if ok then io.stdout:write('NATIVE_SMOKE_OK\n') else io.stdout:write('NATIVE_SMOKE_FAILED: '..err..'\n') end
    io.stdout:flush()
    skynet.abort()
end)
