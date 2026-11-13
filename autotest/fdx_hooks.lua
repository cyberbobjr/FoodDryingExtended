-- Food Drying Extended in-game test (pzdev, single player client), nominal path:
--   1. item scripts exist, vanilla items carry the Food Drying tags (and keep their own),
--      OvenDrying.dryableTypes maps them;
--   2. Food Drying's rack recipes (file replaced by the mod) map the new fruit, berries,
--      vegetables and salted seafood; the mod's recipes exist; SaltSeafood maps each seafood;
--   3. trays of the mod with the mod's own OnCreate functions:
--      crisps (potato + kale), crisps with oil (bonus), fruit leather (average), insects,
--      uncooked tray -> raw food back;
--   4. paper bag: empty bag accepted, bag holding an item refused, mood copied to the bag;
--   5. display names (Food Drying's names kept, the mod's names translated).
-- Test items are removed at the end.
local H = {}
local lines, okAll, passed, failed = {}, true, 0, 0

local function rec(ok, name, detail)
    if ok then passed = passed + 1 else okAll = false; failed = failed + 1 end
    lines[#lines + 1] = (ok and "PASS " or "FAIL ") .. name .. (detail and (" - " .. tostring(detail)) or "")
end

local function check(name, fn)
    local ok, res, detail = pcall(fn)
    if not ok then
        rec(false, name, "error: " .. tostring(res))
        return
    end
    rec(res == true, name, detail)
end

local function tag(name)
    return ItemTag.get(ResourceLocation.of(name))
end

local function list(items)
    local a = ArrayList.new()
    for _, it in ipairs(items) do a:add(it) end
    return a
end

-- Minimal craftRecipeData for the OnCreate functions (they only read these two lists).
local function fakeRecipeData(consumed, createdItems)
    local d = {}
    function d:getAllConsumedItems() return list(consumed) end
    function d:getAllCreatedItems() return list(createdItems) end
    return d
end

local function near(a, b)
    return a ~= nil and b ~= nil and math.abs(a - b) < 0.01
end

local TAGGED = {
    ["fooddrying:dryablevegetable"] = { "BrusselSprouts", "Cucumber", "PumpkinSliced", "SweetPotato", "Turnip", "Zucchini",
        "Cabbage", "SugarBeet", "Garlic", "GreenOnions", "PepperJalapeno", "PepperHabanero",
        "Dandelions", "GingerRoot", "GrapeLeaves", "Violets", "Thistle", "Nettles", "LemonGrass", "Ginseng" },
    ["fooddrying:dryablefruit"] = { "WatermelonSliced" },
    ["fooddrying:dryableberries"] = { "Rosehips" },
}

local DRIED = {
    BrusselSprouts = "FoodDryingExtended.BrusselSproutsDried", Cucumber = "FoodDryingExtended.CucumberDried",
    PumpkinSliced = "FoodDryingExtended.PumpkinSlicedDried", SweetPotato = "FoodDryingExtended.SweetPotatoDried",
    Turnip = "FoodDryingExtended.TurnipDried", Zucchini = "FoodDryingExtended.ZucchiniDried",
    Cabbage = "FoodDryingExtended.CabbageDried", SugarBeet = "FoodDryingExtended.SugarBeetDried",
    Garlic = "FoodDryingExtended.GarlicDried", GreenOnions = "FoodDryingExtended.GreenOnionsDried",
    WatermelonSliced = "FoodDryingExtended.WatermelonDried", Rosehips = "FoodDryingExtended.RosehipsDried",
    PepperJalapeno = "Base.PepperJalapenoDried", PepperHabanero = "Base.PepperHabaneroDried",
    Dandelions = "FoodDryingExtended.DandelionsDried", GingerRoot = "FoodDryingExtended.GingerRootDried",
    GrapeLeaves = "FoodDryingExtended.GrapeLeavesDried", Violets = "FoodDryingExtended.VioletsDried",
    Thistle = "FoodDryingExtended.ThistleDried", Nettles = "FoodDryingExtended.NettlesDried",
    LemonGrass = "FoodDryingExtended.LemonGrassDried", Ginseng = "FoodDryingExtended.GinsengDried",
}

local HERBS = { "Basil", "Chives", "Cilantro", "Oregano", "Parsley", "Rosemary", "Sage", "Thyme" }

-- rack recipe -> { result, pattern } pairs added by the mod
local RACK = {
    ["FoodDrying.DryVegetables"] = {
        { "FoodDryingExtended.CucumberDried", "Base.Cucumber" }, { "FoodDryingExtended.CabbageDried", "Base.Cabbage" },
        { "FoodDryingExtended.GarlicDried", "Base.Garlic" }, { "Base.PepperJalapenoDried", "Base.PepperJalapeno" },
        { "FoodDrying.TomatoDried", "Base.Tomato" } },
    ["FoodDrying.DryFruit"] = { { "FoodDryingExtended.WatermelonDried", "Base.WatermelonSliced" },
        { "FoodDrying.AppleDried", "Base.Apple" } },
    ["FoodDrying.DryBerries"] = { { "FoodDryingExtended.RosehipsDried", "Base.Rosehips" } },
    ["FoodDrying.DryFish"] = { { "FoodDryingExtended.ShrimpDried", "FoodDryingExtended.ShrimpSalted" },
        { "FoodDryingExtended.OystersDried", "FoodDryingExtended.OystersSalted" },
        { "FoodDrying.SalmonDried", "FoodDrying.SalmonSalted" } },
    ["FoodDryingExtended.SaltSeafood"] = { { "FoodDryingExtended.SquidSalted", "Base.Squid" },
        { "FoodDryingExtended.CrayfishSalted", "Base.Crayfish" } },
    ["FoodDryingExtended.DryWildPlants"] = { { "FoodDryingExtended.GinsengDried", "Base.Ginseng" },
        { "FoodDryingExtended.NettlesDried", "Base.Nettles" } },
}
table.insert(RACK["FoodDrying.DryVegetables"], { "FoodDryingExtended.DandelionsDried", "Base.Dandelions" })

local function mapperHas(recipeName, resultType, rawType)
    local sm = getScriptManager()
    local recipe = sm:getCraftRecipe(recipeName)
    if not recipe then return false, "recipe missing" end
    local mapper = recipe:getOutputs():get(0):getOutputMapper()
    local result = sm:FindItem(resultType)
    if not result then return false, "result missing" end
    local pattern = mapper:getPatternForResult(result)
    for i = 0, pattern:size() - 1 do
        if pattern:get(i):getFullName() == rawType then return true end
    end
    return false, "pattern without " .. rawType
end

local function scriptChecks()
    local sm = getScriptManager()
    for tagName, names in pairs(TAGGED) do
        for _, n in ipairs(names) do
            check("tag " .. tagName .. " on Base." .. n, function()
                return sm:FindItem("Base." .. n):hasTag(tag(tagName)) == true
            end)
            check("dryableTypes Base." .. n, function()
                local v = OvenDrying.dryableTypes["Base." .. n]
                return v == DRIED[n] and sm:FindItem(v) ~= nil, tostring(v)
            end)
        end
    end
    check("vanilla tags kept (SweetPotato isseed, Rosehips herbaltea, Garlic isseed)", function()
        return sm:FindItem("Base.SweetPotato"):hasTag(tag("base:isseed"))
            and sm:FindItem("Base.Rosehips"):hasTag(tag("base:herbaltea"))
            and sm:FindItem("Base.Garlic"):hasTag(tag("base:isseed"))
    end)
    check("dried rose hips still usable for tea", function()
        return sm:FindItem("FoodDryingExtended.RosehipsDried"):hasTag(tag("base:herbaltea"))
    end)
    check("shelf life tags (driedvegetables, driedfruit, driedfish)", function()
        return sm:FindItem("FoodDryingExtended.CabbageDried"):hasTag(tag("fooddrying:driedvegetables"))
            and sm:FindItem("FoodDryingExtended.FruitLeather"):hasTag(tag("fooddrying:driedfruit"))
            and sm:FindItem("FoodDryingExtended.SquidDried"):hasTag(tag("fooddrying:driedfish"))
            and sm:FindItem("FoodDryingExtended.SquidSalted"):hasTag(tag("fooddrying:saltedfish"))
    end)
    check("potato no longer in Food Drying's oven table", function()
        return OvenDrying.dryableTypes["Base.Potato"] == nil
    end)
    for _, r in ipairs({ "PrepareHomemadeCrispsTray", "PrepareHomemadeCrispsTrayOil", "PrepareFruitLeatherTray",
                         "PrepareRoastedInsectsTray", "EmptyExtendedTray", "BagHomemadeCrisps", "SaltSeafood" }) do
        check("recipe FoodDryingExtended." .. r, function()
            return sm:getCraftRecipe("FoodDryingExtended." .. r) ~= nil
        end)
    end
    check("herb rack recipe DryWildPlants is tagged DryingRackHerb", function()
        local r = sm:getCraftRecipe("FoodDryingExtended.DryWildPlants")
        if not r then return false, "recipe missing" end
        local tags = r:getTags()
        for i = 0, tags:size() - 1 do
            if string.lower(tostring(tags:get(i))) == "dryingrackherb" then return true end
        end
        return false, tostring(tags)
    end)
    check("dried ginger, lemongrass and ginseng still make herbal tea", function()
        local t = tag("base:herbaltea")
        return sm:FindItem("FoodDryingExtended.GingerRootDried"):hasTag(t)
            and sm:FindItem("FoodDryingExtended.LemonGrassDried"):hasTag(t)
            and sm:FindItem("FoodDryingExtended.GinsengDried"):hasTag(t)
    end)
    for _, h in ipairs(HERBS) do
        check("grind recipe: 4 Base." .. h .. "Dried -> Base.Seasoning_" .. h, function()
            local r = sm:getCraftRecipe("FoodDryingExtended.Grind" .. h .. "Seasoning")
            if not r then return false, "recipe missing" end
            local out = r:getOutputs():get(0):getPossibleResultItems()
            local ok = false
            for i = 0, out:size() - 1 do
                if out:get(i):getFullName() == "Base.Seasoning_" .. h then ok = true end
            end
            return ok and sm:FindItem("Base." .. h .. "Dried") ~= nil
        end)
    end
    for recipeName, pairsList in pairs(RACK) do
        for _, p in ipairs(pairsList) do
            check(recipeName .. " maps " .. p[2] .. " -> " .. p[1], function()
                return mapperHas(recipeName, p[1], p[2])
            end)
        end
    end
end

local function fill(trayType, items)
    local inv = getPlayer():getInventory()
    local tray = instanceItem(trayType)
    inv:AddItem(tray)
    FoodDryingExtended.onTrayFilled(fakeRecipeData(items, { tray }), getPlayer())
    return tray
end

-- Empties a tray and returns the new items of the inventory (type -> list).
local function empty(tray)
    local inv = getPlayer():getInventory()
    local before = {}
    local all = inv:getItems()
    for i = 0, all:size() - 1 do before[all:get(i)] = true end
    FoodDryingExtended.onTrayEmptied(fakeRecipeData({ tray }, {}), getPlayer())
    inv:DoRemoveItem(tray)
    local got = {}
    all = inv:getItems()
    for i = all:size() - 1, 0, -1 do
        local it = all:get(i)
        if not before[it] then
            local t = it:getFullType()
            got[t] = got[t] or {}
            table.insert(got[t], it)
            inv:DoRemoveItem(it)
        end
    end
    return got
end

local function count(got, t)
    return got[t] and #got[t] or 0
end

local function trayChecks()
    -- crisps: potato + kale + potato, salt ignored
    local tray = fill("FoodDryingExtended.BakingTrayCrisps",
        { instanceItem("Base.Potato"), instanceItem("Base.Salt"), instanceItem("Base.Kale"), instanceItem("Base.Potato") })
    check("crisps tray: 3 entries (salt ignored)", function()
        local e = tray:getModData().fdxEntries
        return e ~= nil and #e == 3, tostring(e and #e)
    end)
    tray:setCooked(true)
    FoodDryingExtended.onTrayCooked(tray)
    check("cooked tray shows the dried tray model", function()
        return tray:getStaticModel() == "FoodDrying.BakingTrayVegetablesDried", tray:getStaticModel()
    end)
    local got = empty(tray)
    check("crisps: 2 potato crisps + 1 kale crisps", function()
        return count(got, "FoodDryingExtended.HomemadeCrisps") == 2 and count(got, "FoodDryingExtended.KaleCrisps") == 1
    end)
    check("kale crisps keep the kale calories (178)", function()
        local k = got["FoodDryingExtended.KaleCrisps"] and got["FoodDryingExtended.KaleCrisps"][1]
        return k ~= nil and near(k:getCalories(), 178), k and tostring(k:getCalories())
    end)

    -- crisps with oil
    tray = fill("FoodDryingExtended.BakingTrayCrispsOil", { instanceItem("Base.Potato"), instanceItem("Base.OilVegetable") })
    tray:setCooked(true)
    got = empty(tray)
    local c = got["FoodDryingExtended.HomemadeCrisps"] and got["FoodDryingExtended.HomemadeCrisps"][1]
    check("oil crisps: +70 kcal, +8 g lipids, -10 unhappiness", function()
        return c ~= nil and near(c:getCalories(), 140) and near(c:getLipids(), 8.15) and near(c:getUnhappyChange(), -10),
            c and (tostring(c:getCalories()) .. " kcal, " .. tostring(c:getLipids()) .. " g, unhappy " .. tostring(c:getUnhappyChange()))
    end)
    check("oil itself is not turned into crisps", function()
        return count(got, "FoodDryingExtended.HomemadeCrisps") == 1
    end)

    -- bag keeps the oil crisps mood
    if c then
        local bag = instanceItem("FoodDryingExtended.HomemadeCrispsBag")
        FoodDryingExtended.onCrispsBagged(fakeRecipeData({ c, instanceItem("Base.PaperBag") }, { bag }), getPlayer())
        check("bag of crisps keeps the mood of oil crisps", function()
            return near(bag:getUnhappyChange(), -10), tostring(bag:getUnhappyChange())
        end)
    end

    -- fruit leather: average of 2 apples + 2 bananas
    local fruits = { instanceItem("Base.Apple"), instanceItem("Base.Apple"), instanceItem("Base.Banana"), instanceItem("Base.Banana") }
    local total = 0
    for _, f in ipairs(fruits) do total = total + f:getCalories() end
    tray = fill("FoodDryingExtended.BakingTrayFruitLeather", fruits)
    tray:setCooked(true)
    got = empty(tray)
    check("fruit leather: 5 rolls for 64 points of hunger, calories shared", function()
        local l = got["FoodDryingExtended.FruitLeather"]
        return l ~= nil and #l == 5 and near(l[1]:getCalories(), total / 5),
            l and (tostring(#l) .. " x " .. tostring(l[1]:getCalories()) .. " (expected " .. tostring(total / 5) .. ")")
    end)

    -- insects
    tray = fill("FoodDryingExtended.BakingTrayInsects",
        { instanceItem("Base.Cricket"), instanceItem("Base.MonarchCaterpillar"), instanceItem("Base.SilkMothCaterpillar") })
    tray:setCooked(true)
    got = empty(tray)
    check("insects: 1 roasted cricket + 2 roasted caterpillars", function()
        return count(got, "FoodDryingExtended.RoastedCricket") == 1 and count(got, "FoodDryingExtended.RoastedCaterpillar") == 2
    end)

    -- uncooked tray gives the raw food back
    tray = fill("FoodDryingExtended.BakingTrayInsects", { instanceItem("Base.Grasshopper"), instanceItem("Base.Grasshopper") })
    got = empty(tray)
    check("uncooked tray: 2 grasshoppers back", function()
        return count(got, "Base.Grasshopper") == 2
    end)
end

local function bagChecks()
    local bag = instanceItem("Base.PaperBag")
    check("empty paper bag accepted", function()
        return FoodDryingExtended.isEmptyPaperBag(bag, getPlayer()) == true
    end)
    bag:getItemContainer():AddItem(instanceItem("Base.Pencil"))
    check("paper bag holding an item refused", function()
        return FoodDryingExtended.isEmptyPaperBag(bag, getPlayer()) == false
    end)
    check("bag of crisps gives the paper bag back once eaten", function()
        local s = getScriptManager():FindItem("FoodDryingExtended.HomemadeCrispsBag")
        return s ~= nil and s:getReplaceOnUse() == "Base.PaperBag"
    end)
end

local function nameChecks()
    for _, t in ipairs({ "FoodDrying.AppleDried", "FoodDryingExtended.CucumberDried", "FoodDryingExtended.FruitLeather",
                         "FoodDryingExtended.RoastedCricket", "FoodDryingExtended.SquidSalted" }) do
        check("display name of " .. t, function()
            local name = instanceItem(t):getDisplayName()
            local rawName = string.match(t, "%.(.+)$")
            return name ~= nil and name ~= "" and name ~= rawName and not string.find(name, "FoodDrying", 1, true),
                tostring(name)
        end)
    end
end

function H.start(ctx)
    local p = getPlayer()
    if not p then return false, "no player" end
    rec(OvenDrying ~= nil and OvenDrying.dryableTypes ~= nil, "Food Drying loaded (OvenDrying.dryableTypes)")
    rec(FoodDryingExtended ~= nil and FoodDryingExtended.onTrayFilled ~= nil, "mod loaded (FoodDryingExtended)")
    if not OvenDrying or not FoodDryingExtended then return true end
    local ok, err = pcall(function()
        scriptChecks()
        trayChecks()
        bagChecks()
        nameChecks()
    end)
    if not ok then rec(false, "test run", "error: " .. tostring(err)) end
    return true
end

function H.done(ctx)
    return true
end

function H.result(ctx)
    return { ok = okAll, summary = string.format("%d PASS, %d FAIL", passed, failed), lines = lines }
end

return { client = H }
