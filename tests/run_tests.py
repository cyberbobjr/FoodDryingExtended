"""Offline checks of Food Drying Extended (no game needed).

Usage: python tests/run_tests.py   (needs lupa; paths to the vanilla scripts and to Food Drying below)

1. References: every item named in the mod's scripts and Lua exists (vanilla 42.22, Food Drying or this mod).
2. Translations: the 11 languages have exactly the items and recipes of the scripts.
3. Tray logic (FoodDryingExtended.lua run in lupa with small stand-ins of the game objects):
   fruit leather rolls follow the quantity of fruit, crisps and oil bonus, uncooked tray, oven table.
"""
import glob
import json
import os
import re
import sys

from lupa import LuaRuntime

ROOT = os.path.join(os.path.dirname(__file__), "..")
MEDIA = os.path.join(ROOT, "Contents", "mods", "batman_FoodDryingExtended", "42.21", "media")
VANILLA = os.environ.get("PZ_VANILLA_SCRIPTS", r"E:\pz-source-42.22\media\scripts")
FOOD_DRYING = os.environ.get(
    "PZ_FOOD_DRYING", r"D:\SteamLibrary\steamapps\workshop\content\108600\3747396551\mods\FoodDrying\42\media")
LANGS = "EN FR DE ES PT PTBR RU CN JP KO TR".split()
failures = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (" - " + str(detail) if detail and not ok else ""))
    if not ok:
        failures.append(name)


def read(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def items_of(folder):
    names = set()
    for f in glob.glob(os.path.join(folder, "**", "*.txt"), recursive=True):
        names.update(re.findall(r"^\s*item\s+(\w+)\s*$", read(f), re.M))
    return names


def references():
    vanilla = items_of(os.path.join(VANILLA, "generated", "items"))
    food_drying = items_of(os.path.join(FOOD_DRYING, "scripts"))
    mine = set(re.findall(r"^\s*item (\w+)\s*$", read(os.path.join(MEDIA, "scripts", "FoodDryingExtended_items.txt")), re.M))
    models_file = os.path.join(MEDIA, "scripts", "FoodDryingExtended_models.txt")
    models = set(re.findall(r"^\s*model (\w+)\s*$", read(models_file), re.M))
    known = {"Base": vanilla, "FoodDrying": food_drying, "FoodDryingExtended": mine | models}
    # assets of the mod's own models and icons, exact case (the server runs on Linux)
    assets = []
    for mesh in re.findall(r"mesh = (WorldItems/FDX_\w+),", read(models_file)):
        assets.append(os.path.join("models_X", *mesh.split("/")) + ".fbx")
    for tex in re.findall(r"texture = ([\w/]*FDX_\w+),", read(models_file)):
        assets.append(os.path.join("textures", *tex.split("/")) + ".png")
    items_text = read(os.path.join(MEDIA, "scripts", "FoodDryingExtended_items.txt"))
    for icon in re.findall(r"Icon = (FDX_\w+),", items_text):
        assets.append(os.path.join("textures", "Item_" + icon + ".png"))
    absent = []
    for rel in assets:
        folder, name = os.path.split(os.path.join(MEDIA, rel))
        if not os.path.isdir(folder) or name not in os.listdir(folder):
            absent.append(rel)
    check(f"{len(assets)} model, texture and icon files exist with exact case", not absent and len(assets) == 21, absent)
    sources = glob.glob(os.path.join(MEDIA, "scripts", "**", "*.txt"), recursive=True)
    sources.append(os.path.join(MEDIA, "lua", "shared", "FoodDryingExtended.lua"))
    fd_lua = "".join(read(f) for f in glob.glob(os.path.join(FOOD_DRYING, "lua", "shared", "*.lua")))
    missing = set()
    for f in sources:
        text = read(f)
        for module, name in re.findall(r"\b(Base|FoodDryingExtended|FoodDrying)\.(\w+)", text):
            # Lua identifiers and model names are not items
            if module != "Base" and (name[0].islower() or name.isupper() or name.startswith(("BakingTray", "Skewer")) and module == "FoodDrying"):
                continue
            if name not in known[module]:
                # a Lua function of Food Drying (OnCreate / OnTest of a recipe)
                if module == "FoodDrying" and ("function FoodDrying." + name + "(") in fd_lua:
                    continue
                missing.add(module + "." + name)
    # vanilla items given a tag by the mod
    for name in re.findall(r"^\s*item (\w+)\s*$", read(os.path.join(MEDIA, "scripts", "FoodDryingExtended_vanilla_overrides.txt")), re.M):
        if name not in vanilla:
            missing.add("Base." + name + " (override)")
    check("every referenced item exists", not missing, sorted(missing))
    return mine


def translations(mine):
    recipes = set(re.findall(r"craftRecipe (\w+)", read(os.path.join(MEDIA, "scripts", "FoodDryingExtended_recipes.txt"))))
    for lang in LANGS:
        folder = os.path.join(MEDIA, "lua", "shared", "Translate", lang)
        names = {k.split(".", 1)[1] for k in json.loads(read(os.path.join(folder, "ItemName.json")))}
        labels = set(json.loads(read(os.path.join(folder, "Recipes.json"))))
        check(f"translations {lang} match the scripts", names == mine and labels == recipes,
              sorted((names ^ mine) | (labels ^ recipes)))


STUBS = r"""
given = {}
local function food(fullType, hunger, calories, lipids, isFood)
    local it = { _type = fullType, _hunger = hunger, _cal = calories, _carb = 1, _lip = lipids or 0, _prot = 1,
                 _unhappy = 0, _age = 0, _cooked = false, _md = {}, _isFood = isFood ~= false }
    function it:getFullType() return self._type end
    function it:getHungerChange() return self._hunger end
    function it:getCalories() return self._cal end
    function it:getCarbohydrates() return self._carb end
    function it:getLipids() return self._lip end
    function it:getProteins() return self._prot end
    function it:getUnhappyChange() return self._unhappy end
    function it:getOffAgeMax() return 10 end
    function it:getAge() return self._age end
    function it:getPoisonPower() return 0 end
    function it:getPoisonDetectionLevel() return 0 end
    function it:setHungChange(v) self._hunger = v end
    function it:setCalories(v) self._cal = v end
    function it:setCarbohydrates(v) self._carb = v end
    function it:setLipids(v) self._lip = v end
    function it:setProteins(v) self._prot = v end
    function it:setUnhappyChange(v) self._unhappy = v end
    function it:setAge(v) self._age = v end
    function it:getModData() return self._md end
    function it:syncItemFields() end
    function it:isCooked() return self._cooked end
    return it
end
RAW = {
    ["Base.Pineapple"] = { -0.24, 452 }, ["Base.Cherry"] = { -0.03, 5 }, ["Base.Apple"] = { -0.16, 95 },
    ["Base.Peach"] = { -0.12, 58 }, ["Base.Potato"] = { -0.18, 70, 0.15 }, ["Base.Kale"] = { -0.16, 178, 0.71 },
    ["Base.Lard"] = { -0.24, 4095, 454 }, ["FoodDrying.BeefDried"] = { -0.80, 440, 18.7 },
    ["FoodDrying.SmallbirdmeatDried"] = { -0.10, 60, 2 }, ["FoodDrying.BerryBlueDried"] = { -0.05, 30 },
}
function newFood(t) local r = RAW[t] or { -0.10, 10 }; return food(t, r[1], r[2], r[3]) end
function newTray(t) return food(t, 0, 0, 0) end
function instanceItem(t) return newFood(t) end
function instanceof(obj, class) return class == "Food" and obj._isFood end
function sendAddItemToContainer() end
function require() end
function print() end
function getScriptManager() return { FindItem = function() return true end } end
OvenDrying = { dryableTypes = { ["Base.Pineapple"] = "FoodDrying.PineappleDried", ["Base.Apple"] = "FoodDrying.AppleDried" } }
player = { getInventory = function() return { AddItem = function(_, it) given[#given + 1] = it end } end }
local function list(t)
    return { size = function() return #t end, get = function(_, i) return t[i + 1] end }
end
function data(consumed, created)
    return { getAllConsumedItems = function() return list(consumed) end,
             getAllCreatedItems = function() return list(created) end }
end
-- fills a tray with raw types, cooks it when asked, empties it; returns the items given to the player
function cycle(trayType, rawTypes, cooked, extra)
    given = {}
    local tray = newTray(trayType)
    local consumed = {}
    for _, t in ipairs(rawTypes) do consumed[#consumed + 1] = newFood(t) end
    if extra then consumed[#consumed + 1] = food(extra, -0.30, 2120, 130) end
    FoodDryingExtended.onTrayFilled(data(consumed, { tray }), player)
    tray._cooked = cooked
    FoodDryingExtended.onTrayEmptied(data({ tray }, {}), player)
    return given
end
"""


def tray_logic():
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute(STUBS)
    lua.execute(read(os.path.join(MEDIA, "lua", "shared", "FoodDryingExtended.lua")))
    cycle = lua.globals().cycle
    g = lua.globals()

    check("whole pineapple, mango and grapefruit leave Food Drying's oven table",
          g.OvenDrying.dryableTypes["Base.Pineapple"] is None and g.OvenDrying.dryableTypes["Base.Apple"] is not None)
    check("slices and pumpkin slices are in the oven table",
          g.OvenDrying.dryableTypes["FoodDryingExtended.PineappleSlice"] == "FoodDryingExtended.PineappleSliceDried"
          and g.OvenDrying.dryableTypes["Base.PumpkinSliced"] == "FoodDryingExtended.PumpkinSlicedDried"
          and g.OvenDrying.dryableTypes["Base.Pumpkin"] is None)

    leather = "FoodDryingExtended.BakingTrayFruitLeather"
    for label, fruits, rolls in [
        ("1 pineapple -> 2 rolls", ["Base.Pineapple"], 2),
        ("4 cherries -> 1 roll", ["Base.Cherry"] * 4, 1),
        ("1 cherry -> 1 roll", ["Base.Cherry"], 1),
        ("2 apples + 1 peach -> 4 rolls", ["Base.Apple", "Base.Apple", "Base.Peach"], 4),
        ("4 pineapples -> 8 rolls", ["Base.Pineapple"] * 4, 8),
    ]:
        out = list(cycle(leather, lua.table_from(fruits), True).values())
        total = sum(lua.globals().RAW[f][2] for f in fruits)
        ok = (len(out) == rolls and all(o._type == "FoodDryingExtended.FruitLeather" for o in out)
              and abs(sum(o._cal for o in out) - total) < 0.01)
        check("fruit leather: " + label + ", calories kept", ok, [(o._type, o._cal) for o in out])

    out = list(cycle(leather, lua.table_from(["Base.Pineapple", "Base.Cherry"]), False).values())
    check("uncooked leather tray gives the fruit back", sorted(o._type for o in out) == ["Base.Cherry", "Base.Pineapple"])

    lua.execute("""
        getPlayer = function() return nil end  -- dedicated server
        local tray = newTray("FoodDryingExtended.BakingTrayCrisps")
        FoodDryingExtended.onTrayFilled(data({ newFood("Base.Potato") }, { tray }), player)
        tray._cooked = true
        noCharacterOk = pcall(FoodDryingExtended.onTrayEmptied, data({ tray }, {}), nil)
    """)
    check("emptying without a character (dedicated server) does not raise an error", g.noCharacterOk is True)

    lua.execute("""
        function pemmican(types, character)
            given = {}
            local consumed = {}
            for _, t in ipairs(types) do consumed[#consumed + 1] = newFood(t) end
            local bar = newFood("FoodDryingExtended.Pemmican")
            FoodDryingExtended.onPemmicanMade(data(consumed, { bar }), character)
            local bars = { bar }
            for _, it in ipairs(given) do bars[#bars + 1] = it end
            return bars
        end
    """)
    fat = 4095 * 6 / 24  # 6 uses of a 24-use block of lard
    for label, types, bars, kcal in [
        ("1 dried beef (80 pts) + lard -> 4 bars", ["FoodDrying.BeefDried", "Base.Lard"], 4, 440 + fat),
        ("1 dried small bird (10 pts) + lard -> 1 bar", ["FoodDrying.SmallbirdmeatDried", "Base.Lard"], 1, 60 + fat),
        ("beef + small bird + blueberries + lard -> 5 bars",
         ["FoodDrying.BeefDried", "FoodDrying.SmallbirdmeatDried", "FoodDrying.BerryBlueDried", "Base.Lard"], 5,
         440 + 60 + 30 + fat),
    ]:
        out = list(g.pemmican(lua.table_from(types), g.player).values())
        ok = (len(out) == bars and all(o._type == "FoodDryingExtended.Pemmican" for o in out)
              and abs(sum(o._cal for o in out) - kcal) < 0.01)
        check("pemmican: " + label + ", calories of meat, fat and berries kept", ok, [(o._type, o._cal) for o in out])
    out = list(g.pemmican(lua.table_from(["FoodDrying.BeefDried", "Base.Lard"]), None).values())
    check("pemmican without a character: one bar, no error", len(out) == 1, len(out))

    out = list(cycle("FoodDryingExtended.BakingTrayCrisps", lua.table_from(["Base.Potato", "Base.Kale"]), True).values())
    check("crisps: one portion per vegetable with its calories",
          sorted((o._type, o._cal) for o in out) == [("FoodDryingExtended.HomemadeCrisps", 70), ("FoodDryingExtended.KaleCrisps", 178)])

    out = list(cycle("FoodDryingExtended.BakingTrayCrispsOil", lua.table_from(["Base.Potato"]), True, "Base.OilVegetable").values())
    check("oil crisps: +70 kcal, +8 g lipids, -10 unhappiness, oil not turned into crisps",
          len(out) == 1 and abs(out[0]._cal - 140) < 0.01 and abs(out[0]._lip - 8.15) < 0.01 and out[0]._unhappy == -10,
          [(o._type, o._cal, o._lip, o._unhappy) for o in out])


def main():
    mine = references()
    translations(mine)
    tray_logic()
    print(f"{'OK' if not failures else 'FAILED'}: {len(failures)} failure(s)")
    sys.exit(1 if failures else 0)


main()
