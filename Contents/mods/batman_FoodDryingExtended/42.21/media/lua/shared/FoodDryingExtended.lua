-- Food Drying Extended: adds vegetables and homemade crisps to Food Drying.
--
-- Oven and skewer drying: Food Drying fills trays and skewers from the
-- fooddrying:dryablevegetable tag (added to the vanilla vegetables in
-- FoodDryingExtended_vanilla_overrides.txt) and turns each raw item into its
-- dried type through OvenDrying.dryableTypes, a table Food Drying keeps public
-- for compatibility patches. Each entry is only added when both item scripts
-- exist.
--
-- Drying rack: the rack recipe file of Food Drying is replaced by a copy whose
-- DryVegetables mapper also lists these vegetables (same relative path).

require "OvenDrying"

FoodDryingExtended = FoodDryingExtended or {}

local rawToDried = {
    ["Base.BrusselSprouts"] = "FoodDryingExtended.BrusselSproutsDried",
    ["Base.Cucumber"] = "FoodDryingExtended.CucumberDried",
    ["Base.Pumpkin"] = "FoodDryingExtended.PumpkinDried",
    ["Base.SweetPotato"] = "FoodDryingExtended.SweetPotatoDried",
    ["Base.Turnip"] = "FoodDryingExtended.TurnipDried",
    ["Base.Zucchini"] = "FoodDryingExtended.ZucchiniDried",
    -- Homemade crisps tray: one potato gives one portion of crisps.
    ["Base.Potato"] = "FoodDryingExtended.HomemadeCrisps",
}

local scriptManager = getScriptManager()
for rawType, driedType in pairs(rawToDried) do
    if OvenDrying and OvenDrying.dryableTypes and scriptManager:FindItem(rawType) and scriptManager:FindItem(driedType) then
        OvenDrying.dryableTypes[rawType] = driedType
    else
        print("FOODDRYINGEXTENDED WARNING: could not register " .. rawType .. " -> " .. driedType)
    end
end

-- OnCooked of the crisps tray: show the dried tray model. The name keeps the
-- vanilla cooked prefix, translated on each client.
function FoodDryingExtended.onCrispsTrayCooked(item)
    item:setStaticModel("FoodDrying.BakingTrayVegetablesDried")
    item:setWorldStaticModel("FoodDrying.BakingTrayVegetablesDried")
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
