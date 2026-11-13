-- Food Drying Extended in-game test (pzdev, single player client), nominal path:
--   1. item scripts of the mod exist, the six vanilla vegetables carry the
--      fooddrying:dryablevegetable tag and keep their own tags;
--   2. OvenDrying.dryableTypes maps each vegetable and the potato;
--   3. Food Drying's rack recipe (file replaced by the mod) maps each new vegetable;
--   4. the three crisps recipes exist;
--   5. crisps tray cycle with Food Drying's OnCreate functions: 3 potatoes in the tray,
--      cooked tray emptied -> 3 homemade crisps; uncooked tray -> potatoes back;
--   6. paper bag test: empty bag accepted, bag holding an item refused.
-- Test items are removed at the end.
local H = {}
local lines, okAll, passed, failed = {}, true, 0, 0
local created = {}

local function rec(ok, name, detail)
    if ok then passed = passed + 1 else okAll = false; failed = failed + 1 end
    lines[#lines + 1] = (ok and "PASS " or "FAIL ") .. name .. (detail and (" - " .. tostring(detail)) or "")
end

local function info(msg)
    lines[#lines + 1] = "INFO " .. msg
end

local function check(name, fn)
    local ok, res, detail = pcall(fn)
    if not ok then
        rec(false, name, "error: " .. tostring(res))
        return
    end
    rec(res == true, name, detail)
end

local VEG = { "BrusselSprouts", "Cucumber", "Pumpkin", "SweetPotato", "Turnip", "Zucchini" }

local function tag(name)
    return ItemTag.get(ResourceLocation.of(name))
end

local function newItem(fullType)
    local item = instanceItem(fullType)
    created[#created + 1] = item
    return item
end

local function list(items)
    local a = ArrayList.new()
    for _, it in ipairs(items) do a:add(it) end
    return a
end

-- Minimal craftRecipeData for Food Drying's OnCreate functions (they only read these two lists).
local function fakeRecipeData(consumed, createdItems)
    local d = {}
    function d:getAllConsumedItems() return list(consumed) end
    function d:getAllCreatedItems() return list(createdItems) end
    return d
end

local function countType(inv, fullType)
    return inv:getCountTypeRecurse(fullType)
end

local function removeAll(inv, fullType)
    local items = inv:getAllTypeRecurse(fullType)
    for i = items:size() - 1, 0, -1 do
        local it = items:get(i)
        if it:getContainer() then it:getContainer():DoRemoveItem(it) end
    end
end

local function scriptChecks()
    local sm = getScriptManager()
    for _, n in ipairs(VEG) do
        check("item FoodDryingExtended." .. n .. "Dried", function()
            return sm:FindItem("FoodDryingExtended." .. n .. "Dried") ~= nil
        end)
        check("tag fooddrying:dryablevegetable on Base." .. n, function()
            return sm:FindItem("Base." .. n):hasTag(tag("fooddrying:dryablevegetable")) == true
        end)
        check("dryableTypes Base." .. n, function()
            local v = OvenDrying.dryableTypes["Base." .. n]
            return v == "FoodDryingExtended." .. n .. "Dried", tostring(v)
        end)
    end
    check("vanilla tags kept (SweetPotato base:isseed, Zucchini base:hideuncooked)", function()
        return sm:FindItem("Base.SweetPotato"):hasTag(tag("base:isseed"))
            and sm:FindItem("Base.Zucchini"):hasTag(tag("base:hideuncooked"))
    end)
    check("dried vegetables carry fooddrying:driedvegetables", function()
        return sm:FindItem("FoodDryingExtended.CucumberDried"):hasTag(tag("fooddrying:driedvegetables"))
    end)
    -- Translation files of the same name are merged by key: Food Drying's names stay.
    for _, t in ipairs({ "FoodDrying.AppleDried", "FoodDrying.TomatoDried", "FoodDryingExtended.CucumberDried",
                         "FoodDryingExtended.HomemadeCrispsBag" }) do
        check("display name of " .. t, function()
            local name = instanceItem(t):getDisplayName()
            local rawName = string.match(t, "%.(.+)$")
            return name ~= nil and name ~= "" and name ~= rawName
                and not string.find(name, "FoodDrying", 1, true), tostring(name)
        end)
    end
    check("dryableTypes Base.Potato -> HomemadeCrisps", function()
        return OvenDrying.dryableTypes["Base.Potato"] == "FoodDryingExtended.HomemadeCrisps"
    end)
    for _, r in ipairs({ "PrepareHomemadeCrispsTray", "EmptyHomemadeCrispsTray", "BagHomemadeCrisps" }) do
        check("recipe FoodDryingExtended." .. r, function()
            return sm:getCraftRecipe("FoodDryingExtended." .. r) ~= nil
        end)
    end
    check("rack recipe FoodDrying.DryVegetables maps the new vegetables", function()
        local recipe = sm:getCraftRecipe("FoodDrying.DryVegetables")
        if not recipe then return false, "recipe missing" end
        local mapper = recipe:getOutputs():get(0):getOutputMapper()
        local missing = {}
        for _, n in ipairs(VEG) do
            local result = sm:FindItem("FoodDryingExtended." .. n .. "Dried")
            local pattern = result and mapper:getPatternForResult(result)
            local found = false
            if pattern then
                for i = 0, pattern:size() - 1 do
                    if pattern:get(i):getFullName() == "Base." .. n then found = true end
                end
            end
            if not found then missing[#missing + 1] = n end
        end
        local tomato = sm:FindItem("FoodDrying.TomatoDried")
        local tomatoOk = tomato and mapper:getPatternForResult(tomato):size() > 0
        return #missing == 0 and tomatoOk == true,
            "missing: " .. table.concat(missing, ",") .. " tomato kept: " .. tostring(tomatoOk)
    end)
end

local function crispsCycle(inv)
    -- cooked tray
    local potatoes = { newItem("Base.Potato"), newItem("Base.Potato"), newItem("Base.Potato") }
    local salt = newItem("Base.Salt")
    local tray = newItem("FoodDryingExtended.BakingTrayCrisps")
    inv:AddItem(tray)
    OvenDrying.onContainerFilled(fakeRecipeData({ potatoes[1], potatoes[2], salt, potatoes[3] }, { tray }), getPlayer())
    local data = tray:getModData().poisonData
    check("tray filled: 3 potato entries (salt ignored)", function()
        return data ~= nil and #data == 3, tostring(data and #data)
    end)
    tray:setCooked(true)
    FoodDryingExtended.onCrispsTrayCooked(tray)
    check("cooked tray shows the dried tray model", function()
        return tray:getStaticModel() == "FoodDrying.BakingTrayVegetablesDried", tray:getStaticModel()
    end)
    local before = countType(inv, "FoodDryingExtended.HomemadeCrisps")
    OvenDrying.onContainerEmptied(fakeRecipeData({ tray }, {}), getPlayer())
    local got = countType(inv, "FoodDryingExtended.HomemadeCrisps") - before
    check("cooked tray emptied: 3 homemade crisps", function() return got == 3, tostring(got) end)
    local crisps = inv:getFirstTypeRecurse("FoodDryingExtended.HomemadeCrisps")
    check("crisps keep the potato hunger (-18) and 70 calories", function()
        if not crisps then return false, "no crisps" end
        local h = math.floor(crisps:getHungerChange() * 100 + 0.5)
        return h == -18 and math.floor(crisps:getCalories() + 0.5) == 70,
            "hunger " .. tostring(crisps:getHungerChange()) .. " calories " .. tostring(crisps:getCalories())
    end)
    inv:DoRemoveItem(tray)

    -- uncooked tray gives the potatoes back
    local raw = { newItem("Base.Potato"), newItem("Base.Potato") }
    local tray2 = newItem("FoodDryingExtended.BakingTrayCrisps")
    inv:AddItem(tray2)
    OvenDrying.onContainerFilled(fakeRecipeData(raw, { tray2 }), getPlayer())
    local potBefore = countType(inv, "Base.Potato")
    OvenDrying.onContainerEmptied(fakeRecipeData({ tray2 }, {}), getPlayer())
    local potGot = countType(inv, "Base.Potato") - potBefore
    check("uncooked tray emptied: 2 potatoes back", function() return potGot == 2, tostring(potGot) end)
    inv:DoRemoveItem(tray2)
end

local function bagChecks()
    local bag = newItem("Base.PaperBag")
    check("empty paper bag accepted", function()
        return FoodDryingExtended.isEmptyPaperBag(bag, getPlayer()) == true
    end)
    bag:getItemContainer():AddItem(newItem("Base.Pencil"))
    check("paper bag holding an item refused", function()
        return FoodDryingExtended.isEmptyPaperBag(bag, getPlayer()) == false
    end)
    check("other inputs pass the bag test", function()
        return FoodDryingExtended.isEmptyPaperBag(newItem("FoodDryingExtended.HomemadeCrisps"), getPlayer()) == true
    end)
    check("bag of crisps gives the paper bag back once eaten", function()
        local s = getScriptManager():FindItem("FoodDryingExtended.HomemadeCrispsBag")
        return s ~= nil and s:getReplaceOnUse() == "Base.PaperBag", s and tostring(s:getReplaceOnUse())
    end)
end

function H.start(ctx)
    local p = getPlayer()
    if not p then return false, "no player" end
    rec(OvenDrying ~= nil and OvenDrying.dryableTypes ~= nil, "Food Drying loaded (OvenDrying.dryableTypes)")
    rec(FoodDryingExtended ~= nil and FoodDryingExtended.onCrispsTrayCooked ~= nil, "mod loaded (FoodDryingExtended)")
    if not OvenDrying or not FoodDryingExtended then return true end
    local inv = p:getInventory()
    local ok, err = pcall(function()
        scriptChecks()
        crispsCycle(inv)
        bagChecks()
    end)
    if not ok then rec(false, "test run", "error: " .. tostring(err)) end
    removeAll(inv, "FoodDryingExtended.HomemadeCrisps")
    removeAll(inv, "Base.Potato")
    return true
end

function H.done(ctx)
    return true
end

function H.result(ctx)
    return { ok = okAll, summary = string.format("%d PASS, %d FAIL", passed, failed), lines = lines }
end

return { client = H }
