-- Exercise the real wrapper with an isolated Skynet facade; no game/native license is needed.
local skipped, aborted, requested, logged
package.preload.skynet = function()
    return {
        getenv = function(name) assert(name == 'skip_license_check'); return skipped end,
        abort = function() aborted = true end,
        error = function() logged = true end,
    }
end
package.preload.llicense = function()
    requested = true
    error('license module unavailable in this fixture')
end
local check = dofile('Server/GameServer/services/license_check.lua')
for _, value in ipairs({'true', 'false', 'TRUE', ''}) do
    skipped, aborted, requested, logged = value, false, false, false
    check.check_or_abort()
    assert(logged)
    if value == 'true' then
        assert(not requested and not aborted, 'explicit development mode must avoid native dependency')
    else
        assert(requested and aborted, 'other values must preserve the default check')
    end
    package.loaded.llicense = nil
end
skipped, aborted, requested = nil, false, false
check.check_or_abort()
assert(requested and aborted, 'unset configuration must retain the default check')
print('PASS: 5 license startup configuration cases')
