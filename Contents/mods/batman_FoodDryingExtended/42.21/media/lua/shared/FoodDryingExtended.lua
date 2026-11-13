-- Food Drying Extended: more food for Food Drying.
--
-- Oven trays and skewers of Food Drying: vanilla items get the Food Drying
-- tags (FoodDryingExtended_vanilla_overrides.txt) and their dried type is
-- added to OvenDrying.dryableTypes, a table Food Drying keeps public for
-- compatibility patches. Each entry is only added when both item scripts exist.
--
-- Drying rack: the rack recipes file of Food Drying is replaced by a copy whose
-- mappers also list the items of this mod (same relative path).
--
-- Own oven trays (crisps, crisps with oil, fruit leather, roasted insects):
-- onTrayFilled stores one entry per food put in the tray (type, nutrition,
-- freshness, poison) in the tray's ModData; onTrayEmptied gives the cooked food
-- back (or the raw food when the tray was not cooked).

require "OvenDrying"

FoodDryingExtended = FoodDryingExtended or {}

local rawToDried = {
    ["Base.BrusselSprouts"] = "FoodDryingExtended.BrusselSproutsDried",
    ["Base.Cucumber"] = "FoodDryingExtended.CucumberDried",
    ["Base.PumpkinSliced"] = "FoodDryingExtended.PumpkinSlicedDried",
    ["FoodDryingExtended.PineappleSlice"] = "FoodDryingExtended.PineappleSliceDried",
    ["FoodDryingExtended.MangoSlice"] = "FoodDryingExtended.MangoSliceDried",
    ["FoodDryingExtended.GrapefruitSlice"] = "FoodDryingExtended.GrapefruitSliceDried",
    ["Base.SweetPotato"] = "FoodDryingExtended.SweetPotatoDried",
    ["Base.Turnip"] = "FoodDryingExtended.TurnipDried",
    ["Base.Zucchini"] = "FoodDryingExtended.ZucchiniDried",
    ["Base.Cabbage"] = "FoodDryingExtended.CabbageDried",
    ["Base.SugarBeet"] = "FoodDryingExtended.SugarBeetDried",
    ["Base.Garlic"] = "FoodDryingExtended.GarlicDried",
    ["Base.GreenOnions"] = "FoodDryingExtended.GreenOnionsDried",
    ["Base.WatermelonSliced"] = "FoodDryingExtended.WatermelonDried",
    ["Base.Rosehips"] = "FoodDryingExtended.RosehipsDried",
    ["Base.Dandelions"] = "FoodDryingExtended.DandelionsDried",
    ["Base.GingerRoot"] = "FoodDryingExtended.GingerRootDried",
    ["Base.GrapeLeaves"] = "FoodDryingExtended.GrapeLeavesDried",
    ["Base.Violets"] = "FoodDryingExtended.VioletsDried",
    ["Base.Thistle"] = "FoodDryingExtended.ThistleDried",
    ["Base.Nettles"] = "FoodDryingExtended.NettlesDried",
    ["Base.LemonGrass"] = "FoodDryingExtended.LemonGrassDried",
    ["Base.Ginseng"] = "FoodDryingExtended.GinsengDried",
    -- the game already has dried chili peppers (herb drying rack)
    ["Base.PepperJalapeno"] = "Base.PepperJalapenoDried",
    ["Base.PepperHabanero"] = "Base.PepperHabaneroDried",
}

local scriptManager = getScriptManager()
for rawType, driedType in pairs(rawToDried) do
    if OvenDrying and OvenDrying.dryableTypes and scriptManager:FindItem(rawType) and scriptManager:FindItem(driedType) then
        OvenDrying.dryableTypes[rawType] = driedType
    else
        print("FOODDRYINGEXTENDED WARNING: could not register " .. rawType .. " -> " .. driedType)
    end
end

-- Large fruits are sliced before drying (SliceLargeFruit): the whole fruits lose
-- Food Drying's dryable tag (copy of its VanillaFruitOverrides.txt) and its
-- oven entries.
if OvenDrying and OvenDrying.dryableTypes then
    OvenDrying.dryableTypes["Base.Pineapple"] = nil
    OvenDrying.dryableTypes["Base.Mango"] = nil
    OvenDrying.dryableTypes["Base.Grapefruit"] = nil
end

-- Oil absorbed by one portion of crisps fried with oil. The recipe uses 8 uses
-- of oil (8 % of a bottle, about 560 kcal of vegetable oil) for at most 8
-- portions, so the bonus never exceeds the oil consumed.
FoodDryingExtended.OIL_CALORIES = 70
FoodDryingExtended.OIL_LIPIDS = 8
FoodDryingExtended.OIL_UNHAPPY = -10

local CRISPS = {
    ["Base.Potato"] = "FoodDryingExtended.HomemadeCrisps",
    ["Base.SweetPotato"] = "FoodDryingExtended.SweetPotatoCrisps",
    ["Base.SugarBeet"] = "FoodDryingExtended.SugarBeetCrisps",
    ["Base.Zucchini"] = "FoodDryingExtended.ZucchiniCrisps",
    ["Base.Kale"] = "FoodDryingExtended.KaleCrisps",
}

local INSECTS = {
    ["Base.Cricket"] = "FoodDryingExtended.RoastedCricket",
    ["Base.Grasshopper"] = "FoodDryingExtended.RoastedGrasshopper",
    ["Base.SawflyLarva"] = "FoodDryingExtended.RoastedSawflyLarva",
    ["Base.AmericanLadyCaterpillar"] = "FoodDryingExtended.RoastedCaterpillar",
    ["Base.BandedWoolyBearCaterpillar"] = "FoodDryingExtended.RoastedCaterpillar",
    ["Base.MonarchCaterpillar"] = "FoodDryingExtended.RoastedCaterpillar",
    ["Base.SilkMothCaterpillar"] = "FoodDryingExtended.RoastedCaterpillar",
    ["Base.SwallowtailCaterpillar"] = "FoodDryingExtended.RoastedCaterpillar",
}

-- Fruit leather: one roll per 12 points of hunger of fruit put in the tray
-- (at least one), so the number of rolls follows the quantity of fruit, not the
-- number of fruits.
FoodDryingExtended.LEATHER_HUNGER_PER_ROLL = 12

-- Tray type -> how its content is turned into food.
--   map: raw type -> cooked type (one output per input)
--   pooled: the inputs are pooled into rolls of `pooled` (see LEATHER_HUNGER_PER_ROLL)
--   oil: oil bonus added to each portion
--   cookedModel: model shown once cooked
FoodDryingExtended.TRAYS = {
    ["FoodDryingExtended.BakingTrayCrisps"] = { map = CRISPS, cookedModel = "FoodDrying.BakingTrayVegetablesDried" },
    ["FoodDryingExtended.BakingTrayCrispsOil"] = { map = CRISPS, oil = true, cookedModel = "FoodDrying.BakingTrayVegetablesDried" },
    ["FoodDryingExtended.BakingTrayFruitLeather"] = { pooled = "FoodDryingExtended.FruitLeather", cookedModel = "FoodDrying.BakingTrayFruitDried" },
    ["FoodDryingExtended.BakingTrayInsects"] = { map = INSECTS, cookedModel = "FoodDrying.BakingTrayMushroomsDried" },
}

local function accepts(config, item)
    if not instanceof(item, "Food") then return false end
    if config.map then return config.map[item:getFullType()] ~= nil end
    -- pooled tray: the recipe only takes fruit, every food put in counts
    return config.pooled ~= nil
end

local function findTray(items)
    for i = 0, items:size() - 1 do
        local it = items:get(i)
        if FoodDryingExtended.TRAYS[it:getFullType()] then return it end
    end
    return nil
end

-- OnCreate of the Prepare...Tray recipes.
function FoodDryingExtended.onTrayFilled(craftRecipeData, character)
    local consumed = craftRecipeData:getAllConsumedItems()
    local createdItems = craftRecipeData:getAllCreatedItems()
    if not consumed or not createdItems or createdItems:size() == 0 then return end
    local tray = findTray(createdItems)
    local config = tray and FoodDryingExtended.TRAYS[tray:getFullType()]
    if not config then return end

    local entries = {}
    for i = 0, consumed:size() - 1 do
        local item = consumed:get(i)
        if accepts(config, item) then
            local offAgeMax = item:getOffAgeMax()
            entries[#entries + 1] = {
                rawType = item:getFullType(),
                hunger = item:getHungerChange(),
                calories = item:getCalories(),
                carbohydrates = item:getCarbohydrates(),
                lipids = item:getLipids(),
                proteins = item:getProteins(),
                unhappy = item:getUnhappyChange(),
                agedRatio = (offAgeMax and offAgeMax > 0) and (item:getAge() / offAgeMax) or 0,
                poisonPower = item:getPoisonPower(),
                poisonDetection = item:getPoisonDetectionLevel(),
            }
        end
    end
    tray:getModData().fdxEntries = entries
    tray:syncItemFields()
end

local function setNutrition(food, hunger, calories, carbohydrates, lipids, proteins)
    food:setHungChange(hunger)
    food:setCalories(calories)
    food:setCarbohydrates(carbohydrates)
    food:setLipids(lipids)
    food:setProteins(proteins)
end

local function setPoison(food, power, detection)
    if power and power > 0 then
        food:setPoisonPower(power)
        food:setPoisonDetectionLevel(detection or 0)
    end
end

local function give(character, item)
    local inv = character:getInventory()
    inv:AddItem(item)
    sendAddItemToContainer(inv, item)
end

-- Raw food back from an uncooked tray, with its freshness and nutrition.
local function giveRaw(character, entry)
    local item = instanceItem(entry.rawType)
    if not item then
        print("FOODDRYINGEXTENDED ERROR: cannot create " .. tostring(entry.rawType))
        return
    end
    setNutrition(item, entry.hunger, entry.calories, entry.carbohydrates, entry.lipids, entry.proteins)
    item:setAge(item:getOffAgeMax() * (entry.agedRatio or 0))
    setPoison(item, entry.poisonPower, entry.poisonDetection)
    give(character, item)
end

local function giveCooked(character, config, entry)
    local outType = config.map[entry.rawType]
    local item = outType and instanceItem(outType)
    if not item then
        print("FOODDRYINGEXTENDED ERROR: no cooked type for " .. tostring(entry.rawType))
        return
    end
    local calories, lipids = entry.calories, entry.lipids
    if config.oil then
        calories = calories + FoodDryingExtended.OIL_CALORIES
        lipids = lipids + FoodDryingExtended.OIL_LIPIDS
        item:setUnhappyChange(item:getUnhappyChange() + FoodDryingExtended.OIL_UNHAPPY)
    elseif entry.unhappy and config.map == INSECTS then
        item:setUnhappyChange(entry.unhappy)
    end
    setNutrition(item, entry.hunger, calories, entry.carbohydrates, lipids, entry.proteins)
    setPoison(item, entry.poisonPower, entry.poisonDetection)
    give(character, item)
end

local function givePooled(character, config, entries)
    if #entries == 0 then return end
    local sum = { hunger = 0, calories = 0, carbohydrates = 0, lipids = 0, proteins = 0 }
    local poison, detection = 0, 0
    for _, e in ipairs(entries) do
        for k in pairs(sum) do sum[k] = sum[k] + (e[k] or 0) end
        if (e.poisonPower or 0) > poison then
            poison, detection = e.poisonPower, e.poisonDetection or 0
        end
    end
    -- hunger is stored as a negative fraction (-0.24 for 24 points)
    local points = -sum.hunger * 100
    local n = math.max(1, math.floor(points / FoodDryingExtended.LEATHER_HUNGER_PER_ROLL + 0.5))
    for _ = 1, n do
        local item = instanceItem(config.pooled)
        if item then
            setNutrition(item, sum.hunger / n, sum.calories / n, sum.carbohydrates / n, sum.lipids / n, sum.proteins / n)
            -- poison of one bad fruit spreads into the whole batch
            setPoison(item, poison, detection)
            give(character, item)
        end
    end
end

-- OnCreate of EmptyExtendedTray.
function FoodDryingExtended.onTrayEmptied(craftRecipeData, character)
    local consumed = craftRecipeData:getAllConsumedItems()
    if not consumed or consumed:size() == 0 then return end
    local tray = findTray(consumed)
    local config = tray and FoodDryingExtended.TRAYS[tray:getFullType()]
    if not config then return end
    -- EmptyExtendedTray is a hand craft: ISHandcraftAction:performRecipe always passes the character
    -- (also on a server). No getPlayer() fallback: it returns nil on a dedicated server.
    local char = character
    if not char then
        print("FOODDRYINGEXTENDED WARNING: onTrayEmptied called without a character, tray content not given back")
        return
    end
    local entries = tray:getModData().fdxEntries or {}
    if not tray:isCooked() then
        for _, e in ipairs(entries) do giveRaw(char, e) end
    elseif config.pooled then
        givePooled(char, config, entries)
    else
        for _, e in ipairs(entries) do giveCooked(char, config, e) end
    end
end

-- OnCooked of the trays of this mod: show the dried tray model. The name keeps
-- the vanilla cooked prefix, translated on each client.
function FoodDryingExtended.onTrayCooked(item)
    local config = FoodDryingExtended.TRAYS[item:getFullType()]
    if config and config.cookedModel then
        item:setStaticModel(config.cookedModel)
        item:setWorldStaticModel(config.cookedModel)
    end
end

-- Pemmican (MakePemmican, MakePemmicanWithBerries): pounded dried meat bound with
-- fat. One bar per PEMMICAN_HUNGER_PER_BAR points of hunger of meat, berries and
-- fat (at least one), so the number of bars follows the quantity of meat, not the
-- number of pieces. The bars share the nutrition of everything used.
FoodDryingExtended.PEMMICAN_HUNGER_PER_BAR = 20
-- uses of fat consumed by the recipes (item 6 [Base.Lard;Base.Butter])
FoodDryingExtended.PEMMICAN_FAT_USES = 6
FoodDryingExtended.PEMMICAN_FATS = { ["Base.Lard"] = true, ["Base.Butter"] = true }

-- Nutrition of the fat consumed: PEMMICAN_FAT_USES uses of a fresh block of that fat.
local function addFat(sum, fatType)
    local ref = instanceItem(fatType)
    local uses = ref and -ref:getHungerChange() * 100 or 0
    if uses <= 0 then
        print("FOODDRYINGEXTENDED WARNING: unknown pemmican fat " .. tostring(fatType))
        return
    end
    local share = FoodDryingExtended.PEMMICAN_FAT_USES / uses
    sum.hunger = sum.hunger + ref:getHungerChange() * share
    sum.calories = sum.calories + ref:getCalories() * share
    sum.carbohydrates = sum.carbohydrates + ref:getCarbohydrates() * share
    sum.lipids = sum.lipids + ref:getLipids() * share
    sum.proteins = sum.proteins + ref:getProteins() * share
end

-- OnCreate of MakePemmican and MakePemmicanWithBerries.
function FoodDryingExtended.onPemmicanMade(craftRecipeData, character)
    local consumed = craftRecipeData:getAllConsumedItems()
    local createdItems = craftRecipeData:getAllCreatedItems()
    if not consumed or not createdItems or createdItems:size() == 0 then return end
    local bar = createdItems:get(0)
    local sum = { hunger = 0, calories = 0, carbohydrates = 0, lipids = 0, proteins = 0 }
    local poison, detection = 0, 0
    local fatType = "Base.Lard"
    for i = 0, consumed:size() - 1 do
        local item = consumed:get(i)
        if instanceof(item, "Food") then
            if FoodDryingExtended.PEMMICAN_FATS[item:getFullType()] then
                fatType = item:getFullType()
            else
                sum.hunger = sum.hunger + item:getHungerChange()
                sum.calories = sum.calories + item:getCalories()
                sum.carbohydrates = sum.carbohydrates + item:getCarbohydrates()
                sum.lipids = sum.lipids + item:getLipids()
                sum.proteins = sum.proteins + item:getProteins()
                if item:getPoisonPower() > poison then
                    poison, detection = item:getPoisonPower(), item:getPoisonDetectionLevel()
                end
            end
        end
    end
    addFat(sum, fatType)
    local points = -sum.hunger * 100
    local n = math.max(1, math.floor(points / FoodDryingExtended.PEMMICAN_HUNGER_PER_BAR + 0.5))
    if n > 1 and not character then
        -- hand craft: ISHandcraftAction:performRecipe always passes the character
        print("FOODDRYINGEXTENDED WARNING: onPemmicanMade called without a character, one bar made")
        n = 1
    end
    for i = 1, n do
        local item = i == 1 and bar or instanceItem(bar:getFullType())
        if item then
            setNutrition(item, sum.hunger / n, sum.calories / n, sum.carbohydrates / n, sum.lipids / n, sum.proteins / n)
            setPoison(item, poison, detection)
            if i == 1 then item:syncItemFields() else give(character, item) end
        end
    end
end

-- OnTest of BagHomemadeCrisps: only an empty paper bag can become a crisps
-- bag, so nothing stored in it is lost. Other inputs pass.
function FoodDryingExtended.isEmptyPaperBag(item, character)
    if item and item:getFullType() == "Base.PaperBag" and instanceof(item, "InventoryContainer") then
        local inventory = item:getItemContainer()
        return inventory == nil or inventory:isEmpty()
    end
    return true
end

-- OnCreate of BagHomemadeCrisps: InheritFood copies the nutrition; the mood
-- effect of crisps fried with oil is copied here.
function FoodDryingExtended.onCrispsBagged(craftRecipeData, character)
    local consumed = craftRecipeData:getAllConsumedItems()
    local createdItems = craftRecipeData:getAllCreatedItems()
    if not consumed or not createdItems or createdItems:size() == 0 then return end
    local bag = createdItems:get(0)
    for i = 0, consumed:size() - 1 do
        local item = consumed:get(i)
        if instanceof(item, "Food") and item:getFullType() ~= "Base.PaperBag" then
            bag:setUnhappyChange(item:getUnhappyChange())
            bag:syncItemFields()
            return
        end
    end
end
