"""Generates the item scripts of Food Drying Extended from the tables below.

Usage: python source/build_scripts.py
Writes media/scripts/FoodDryingExtended_items.txt and
media/scripts/FoodDryingExtended_vanilla_overrides.txt (nutrition copied from the
vanilla 42.22 items, scripts/generated/items/food.txt).
"""
import os

ROOT = os.path.join(os.path.dirname(__file__), "..", "Contents", "mods", "batman_FoodDryingExtended",
                    "42.21", "media", "scripts")
out = ["module FoodDryingExtended", "{", "    imports", "    {", "        Base,", "    }", ""]


def item(name, fields):
    out.append(f"    item {name}")
    out.append("    {")
    for k, v in fields:
        out.append(f"        {k} = {v},")
    out.append("    }")
    out.append("")


def comment(text):
    out.append(f"    /* {text} */")
    out.append("")


def nut(h, c, cb, l, p):
    return [("HungerChange", f"{h:.1f}"), ("Calories", f"{c:.1f}"), ("Carbohydrates", cb),
            ("Lipids", l), ("Proteins", p)]


def dried(name, icon, smodel, wmodel, h, c, cb, l, p, evo, ft, w, tag, fresh, rotten, extra=()):
    f = [("DisplayCategory", "Food"), ("ItemType", "base:food"), ("Weight", w), ("DaysFresh", fresh),
         ("DaysTotallyRotten", rotten), ("Icon", icon)]
    if evo:
        f.append(("EvolvedRecipe", evo))
    f.append(("FoodType", ft))
    f += nut(h, c, cb, l, p) + list(extra)
    if smodel:
        f.append(("StaticModel", smodel))
    f.append(("WorldStaticModel", wmodel))
    f.append(("Tags", "base:hideuncooked;base:hidecooked;" + tag))
    item(name, f)


VEG = [
    ("BrusselSprouts", "BrusselSprouts", "BrusselSprouts", -20, 119, 20.45, 0.85, 7.95, "Stir fry:9;Pie:9;Salad:9|Cooked", "Vegetables", 0.15),
    ("Cucumber", "Cucumber", "Cucumber", -10, 33, 6.1, 0.63, 2.37, "Soup:10;Stir fry:10;Salad:10;Sandwich:5", "Vegetables", 0.1),
    ("SweetPotato", "SweetPotato", "SweetPotato_Ground", -18, 70, 14.52, 0.15, 2.88, "Soup:18;Stew:18;Pie:18;Stir fry:18;Salad:9|Cooked", "Vegetables", 0.1),
    ("Turnip", "Turnip", "Turnip", -18, 70, 14.52, 0.15, 2.88, "Soup:18;Stew:18;Pie:18;Stir fry:18;Salad:9", "Vegetables", 0.1),
    ("Zucchini", "Zucchini", "Zucchini_Ground", -10, 33, 6.1, 0.63, 2.37, "Pizza:10;Soup:10;Stew:10;Pie:10;Stir fry:10;Salad:10;Rice:10;Pasta:10;Sandwich:5;Omelette:5", "Vegetables", 0.1),
    ("Cabbage", "Cabbage", "Cabbage_Ground", -24, 180, 41.0, 0.7, 9.0, "Soup:12;Stew:12;Stir fry:12;Sandwich:6;Burger:6;Hotdog:6;Salad:12;Taco:6;Burrito:6", "Vegetables", 0.05),
]

# Large fruits are sliced first (Slice Large Fruit, 4 slices each): name, icon, hand model, world model,
# nutrition of ONE slice (a quarter of the vanilla fruit), evolved recipes.
SLICES = [
    ("Pineapple", "Pineapple", "Pineapple_Ground", "Pineapple_Ground", -6, 113.0, 29.68, 0.27, 1.22, "Pizza:6;Cake:6;FruitSalad:6;Pancakes:6;Muffin:6;ConeIcecream:4;PieSweet:6;Oatmeal:4"),
    ("Mango", "Mango", "Mango_Ground", "Mango_Ground", -5, 63.0, 19.68, 0.27, 0.97, "Cake:5;FruitSalad:5;Pancakes:5;Muffin:5;PieSweet:5;Oatmeal:5"),
    ("Grapefruit", "Grapefruit", "Grapefruit_Eat", "Grapefruit_Ground", -5, 3.75, 25.28, 0.95, 4.39, "Salad:5;FruitSalad:5;Pancakes:5;Muffin:5"),
]

SEA = [
    ("Shrimp", "Shrimp", "Shrimp_Ground", -10, 80, 0.0, 7.0, 10.0, "Pizza:10;Soup:10;Stew:10;Pie:10;Stir fry:10;Sandwich:10|Cooked;Burger:10|Cooked;Salad:10|Cooked;Rice:10;Pasta:10;Burrito:10|Cooked;Taco:5|Cooked", 0.1),
    ("Squid", "Squid", "Squid_Ground", -30, 205, 1.0, 13.0, 32.52, "Pizza:15;Soup:15;Stew:15;Pie:15;Stir fry:15;Sandwich:5|Cooked;Burger:10|Cooked;Salad:10|Cooked;Rice:15;Pasta:15;Taco:5|Cooked;Burrito:10|Cooked", 0.2),
    ("Crayfish", "Crayfish", "Crayfish_Ground", -10, 40, 0.0, 2.0, 8.0, "Pizza:10;Soup:10;Stew:10;Pie:10;Stir fry:10;Sandwich:10|Cooked;Burger:10|Cooked;Salad:10|Cooked;Rice:10;Pasta:10;Burrito:10|Cooked;Taco:10|Cooked", 0.2),
    ("Oysters", "Oysters", "Oysters_Ground", -5, 15, 10.0, 4.0, 22.0, "Pizza:5;Soup:5;Stew:5;Pie:5;Stir fry:5;Sandwich:5|Cooked;Burger:5|Cooked;Salad:5|Cooked;Rice:5;Pasta:5", 0.1),
]

TRAYS = [
    ("BakingTrayCrisps", "FoodDrying.BakingTrayVegetables", 40, 90),
    ("BakingTrayCrispsOil", "FoodDrying.BakingTrayVegetables", 40, 90),
    ("BakingTrayFruitLeather", "FoodDrying.BakingTrayFruit", 120, 240),
    ("BakingTrayInsects", "FoodDrying.BakingTrayMushrooms", 30, 70),
]

CRISPS = [
    ("HomemadeCrisps", -18, 70, 15.0, 0.15, 3.0),
    ("SweetPotatoCrisps", -18, 70, 14.52, 0.15, 2.88),
    ("SugarBeetCrisps", -9, 24, 3.0, 0.0, 4.0),
    ("ZucchiniCrisps", -10, 33, 6.1, 0.63, 2.37),
    ("KaleCrisps", -16, 178, 41.41, 0.71, 9.14),
]

INSECTS = [
    ("RoastedCricket", "Cricket", "Cricket_Ground", 20, 1.34, 1.32, 3.6),
    ("RoastedGrasshopper", "Grasshopper", "Grasshopper_Ground", 25, 3.0, 0.24, 5.55),
    ("RoastedSawflyLarva", "Insect_SawflyLarva", "SawflyLarva_Ground", 27, 3.0, 20.24, 27.55),
    ("RoastedCaterpillar", "Insect_AmericanLadyCaterpillar", "AmericanLadyCaterpillar_Ground", 27, 3.0, 20.24, 27.55),
]

# Wild plants: name, icon, world model, hunger, calories, carbs, lipids, proteins, evolved recipes, food type,
# extra tags (kept from the raw plant, without seed/cutting tags)
WILD = [
    ("Dandelions", "DriedHerbs_generic", "DriedHerbs_generic", -5, 25, 5.0, 0.5, 1.5, "Pizza:5;HotDrink:2;Omelette:5;Sandwich:5;Salad:5;Soup:5;Burger:5", "Greens", ""),
    ("GingerRoot", "RootGinger", "Ginger_Ground", -5, 46, 0.44, 2.36, 5.1, "Salad:1;Sandwich:1;Soup:2;Stew:2;Stir fry:2;HotDrink:1", "NoExplicit", "base:herbaltea;"),
    ("GrapeLeaves", "DriedHerbs_generic", "DriedHerbs_generic", -4, 73, 11.0, 2.0, 4.0, "Soup:4;Stew:4;Salad:4;Rice:4;Pie:4;Sandwich:4", "Vegetables", ""),
    ("Violets", "DriedHerbs_generic", "DriedHerbs_generic", -2, 27, 7.0, 0.0, 1.0, "Salad:2;HotDrink:2", "NoExplicit", ""),
    ("Thistle", "DriedHerbs_generic", "DriedHerbs_generic", -4, 45, 18.0, 0.0, 3.0, "Salad:2;HotDrink:2;Soup:2", "Herb", ""),
    ("Nettles", "DriedHerbs_generic", "DriedHerbs_generic", -4, 50, 15.0, 0.0, 2.0, "Salad:2;HotDrink:2;Soup:2", "Herb", ""),
    ("LemonGrass", "DriedHerbs_generic", "DriedHerbs_generic", -1, 0.1, 0.0, 0.0, 0.0, "Soup:1;Stew:1;Stir fry:1;Rice:1;HotDrink:1", "Herb", "base:herbaltea;"),
    ("Ginseng", "Ginseng", "Ginseng", -1, 0.1, 0.0, 0.0, 0.0, "HotDrink:1", "NoExplicit", "base:herbaltea;"),
]

TAGGED = [
    ("fooddrying:dryablevegetable", ["BrusselSprouts", "Cucumber", "PumpkinSliced", "SweetPotato", "Turnip", "Zucchini",
                                     "Cabbage", "SugarBeet", "Garlic", "GreenOnions", "PepperJalapeno", "PepperHabanero"]
     + [w[0] for w in WILD]),
    ("fooddrying:dryablefruit", ["WatermelonSliced"]),
    ("fooddrying:dryableberries", ["Rosehips"]),
]


def main():
    comment("Dried vegetables (oven tray, skewer, drying rack of Food Drying)")
    for n, icon, model, h, c, cb, l, p, evo, ft, w in VEG:
        dried(n + "Dried", icon, model, model, h, c, cb, l, p, evo, ft, w, "fooddrying:driedvegetables", 150, 300,
              [("CustomEatSound", "EatingCrispy")])
    dried("SugarBeetDried", "SugarBeets", "SugarBeet_Ground", "SugarBeet_Ground", -9, 24, 3.0, 0.0, 4.0, None,
          "Vegetables", 0.05, "fooddrying:driedvegetables", 150, 300,
          [("UnhappyChange", "10"), ("CustomEatSound", "EatingCrispy")])
    dried("GarlicDried", "Garlic", "Garlic", "Garlic", -5, 14, 3.27, 0.035, 0.385,
          "Pizza:1;Omelette:1;Soup:1;Stew:1;Pie:1;Stir fry:1;Sandwich:1;Burger:1;Salad:1;Rice:1;Pasta:1;Taco:1;Burrito:1;Toast:1;Bread:1",
          "Herb", 0.05, "fooddrying:driedvegetables", 150, 300, [("Spice", "true")])
    dried("GreenOnionsDried", "HerbChives", None, "GreenOnions", -3, 0.1, 0.0, 0.0, 0.0,
          "Stir fry:1;Pizza:1;Omelette:1;Pasta:1;Salad:1;Sandwich:1;Soup:1;Stew:1;Bread:1;Toast:1;Burger:1",
          "Herb", 0.05, "fooddrying:driedvegetables", 150, 300, [("Spice", "true"), ("EatType", "EatSmall")])

    dried("PumpkinSlicedDried", "Pumpkin_Slice", "PumpkinSlice", "PumpkinSlice", -4, 40, 2.04, 2.06, 3.45,
          "PieSweet:4;Stew:4;Soup:4;Stir fry:4;Stir fry Griddle Pan:4", "NoExplicit", 0.03,
          "fooddrying:driedvegetables", 150, 300, [("CustomEatSound", "EatingCrispy")])

    comment("Slices of large fruits (Slice Large Fruit) and their dried form")
    for n, icon, smodel, wmodel, h, c, cb, l, p, evo in SLICES:
        # own icons and models (source/slices): fresh = game slice shape, dried = thin copy of it
        item(n + "Slice", [("DisplayCategory", "Food"), ("ItemType", "base:food"), ("Weight", "0.1"), ("DaysFresh", "3"),
                           ("DaysTotallyRotten", "5"), ("Icon", f"FDX_{n}Slice"), ("EvolvedRecipe", evo),
                           ("FoodType", "Fruits")]
             + nut(h, c, cb, l, p) + [("CustomEatSound", "EatingFruit"),
                                      ("StaticModel", f"FoodDryingExtended.FDX_{n}Slice"),
                                      ("WorldStaticModel", f"FoodDryingExtended.FDX_{n}Slice_Ground"),
                                      ("Tags", "fooddrying:dryablefruit")])
        dried(n + "SliceDried", f"FDX_{n}SliceDried", f"FoodDryingExtended.FDX_{n}SliceDried",
              f"FoodDryingExtended.FDX_{n}SliceDried", h, c, cb, l, p, evo, "Fruits", 0.03, "fooddrying:driedfruit",
              180, 365, [("CustomEatSound", "EatingFruit")])

    comment("Dried wild plants (oven tray, skewer, drying racks)")
    for n, icon, model, h, c, cb, l, p, evo, ft, tags in WILD:
        dried(n + "Dried", icon, None, model, h, c, cb, l, p, evo, ft, 0.05, tags + "fooddrying:driedvegetables",
              150, 300, [("Spice", "true")] if ft in ("Herb", "NoExplicit") else [])

    comment("Dried fruit and berries")
    dried("WatermelonDried", "WatermelonSliced", "MelonSlice", "WaterMelonSlice_Ground", -6, 135.5, 34.11, 0.67, 2.75,
          "Salad:6;FruitSalad:6;Pancakes:6;Muffin:6", "Fruits", 0.05, "fooddrying:driedfruit", 180, 365,
          [("CustomEatSound", "EatingFruit")])
    dried("RosehipsDried", "Rosehips", "RoseHips", "RoseHips", -6, 81, 19.0, 0.0, 2.0,
          "HotDrink:2;Salad:3;FruitSalad:3;Soup:6;PieSweet:6;Bread:6", "Berry", 0.05,
          "base:herbaltea;fooddrying:driedberries", 180, 365, [("Spice", "true")])

    comment("Seafood: salted (Salt Seafood), then dried on the drying rack like salted fish")
    for n, icon, model, h, c, cb, l, p, evo, w in SEA:
        n5 = nut(h, c, cb, l, p)
        item(n + "Salted", [("DisplayCategory", "Food"), ("ItemType", "base:food"), ("Weight", w), ("Icon", icon),
                            ("BadInMicrowave", "true"), ("DangerousUncooked", "true"), ("EvolvedRecipe", evo),
                            ("FoodType", "Seafood"), ("GoodHot", "true"), ("IsCookable", "true"),
                            ("MinutesToCook", "20"), ("MinutesToBurn", "50"), ("DaysFresh", "4"),
                            ("DaysTotallyRotten", "8"), n5[0], ("ThirstChange", f"{-h:.1f}")] + n5[1:] +
             [("StaticModel", model), ("WorldStaticModel", model), ("Tags", "fooddrying:saltedfish"),
              ("CookingSound", "FryingFood")])
        item(n + "Dried", [("DisplayCategory", "Food"), ("ItemType", "base:food"), ("Weight", round(w / 2, 2)),
                           ("DaysFresh", "120"), ("DaysTotallyRotten", "270"), ("Icon", icon),
                           ("BadInMicrowave", "true"), ("EvolvedRecipe", evo), ("FoodType", "Seafood")] + n5 +
             [("StaticModel", model), ("WorldStaticModel", model), ("Tags", "fooddrying:driedfish")])

    comment("Oven trays of this mod (filled and emptied by FoodDryingExtended.lua)")
    for n, model, cook, burn in TRAYS:
        item(n, [("DisplayCategory", "Food"), ("ItemType", "base:food"), ("Weight", "0.5"), ("Icon", "BakingTrayFruit"),
                 ("IsCookable", "true"), ("CantEat", "true"), ("OnCooked", "FoodDryingExtended.onTrayCooked"),
                 ("MinutesToCook", cook), ("MinutesToBurn", burn), ("HungerChange", "0.0"), ("StaticModel", model),
                 ("WorldStaticModel", model), ("CookingSound", "FryingFood"),
                 ("Tags", "base:hideuncooked;base:hasmetal;base:spawncooked")])

    comment("Homemade crisps (one portion per vegetable, nutrition copied from it)")
    for n, h, c, cb, l, p in CRISPS:
        item(n, [("DisplayCategory", "Food"), ("ItemType", "base:food"), ("EatType", "EatSmall"), ("Weight", "0.05"),
                 ("DaysFresh", "14"), ("DaysTotallyRotten", "30"), ("Icon", "TortillaChips"),
                 ("FoodType", "Vegetables")] + nut(h, c, cb, l, p) +
             [("CustomEatSound", "EatingCrispy"), ("Tags", "base:hideuncooked;base:hidecooked")])
    item("HomemadeCrispsBag", [("DisplayCategory", "Food"), ("ItemType", "base:food"), ("EatType", "EatBox"),
                               ("Weight", "0.15"), ("DaysFresh", "30"), ("DaysTotallyRotten", "60"),
                               ("Icon", "Paperbag"), ("FoodType", "Vegetables")] + nut(-18, 70, 15.0, 0.15, 3.0) +
         [("ReplaceOnUse", "Base.PaperBag"), ("CustomEatSound", "EatingCrispy"), ("StaticModel", "Chips"),
          ("WorldStaticModel", "Paperbag_Ground"), ("Tags", "base:hideuncooked;base:hidecooked")])

    comment("Fruit leather (average nutrition of the fruits used)")
    item("FruitLeather", [("DisplayCategory", "Food"), ("ItemType", "base:food"), ("Weight", "0.05"),
                          ("DaysFresh", "180"), ("DaysTotallyRotten", "365"), ("Icon", "DriedApricots"),
                          ("FoodType", "Fruits")] + nut(-12, 90, 22.0, 0.3, 1.0) +
         [("UnhappyChange", "-10"), ("CustomEatSound", "EatingFruit"), ("StaticModel", "DriedApricot_Hand"),
          ("WorldStaticModel", "DriedApricots"), ("Tags", "base:hideuncooked;base:hidecooked;fooddrying:driedfruit")])

    comment("Roasted insects (nutrition copied from the raw insect)")
    for n, icon, model, c, cb, l, p in INSECTS:
        item(n, [("DisplayCategory", "Food"), ("ItemType", "base:food"), ("Weight", "0.05"), ("DaysFresh", "180"),
                 ("DaysTotallyRotten", "365"), ("Icon", icon), ("FoodType", "Insect")] + nut(-1, c, cb, l, p) +
             [("UnhappyChange", "20"), ("CustomEatSound", "EatingCrispy"), ("StaticModel", model),
              ("WorldStaticModel", model), ("Tags", "base:hideuncooked;base:hidecooked;base:nocookingxp")])
    out.append("}")
    out.append("")
    with open(os.path.join(ROOT, "FoodDryingExtended_items.txt"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out))

    ov = ["module Base", "{"]
    for tag, names in TAGGED:
        for n in names:
            ov += [f"    item {n}", "    {", f"        Tags = {tag},", "    }", ""]
    ov += ["}", ""]
    with open(os.path.join(ROOT, "FoodDryingExtended_vanilla_overrides.txt"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(ov))
    print(sum(1 for l in out if l.startswith("    item ")), "items written")
    write_models()


# Models of the fruit slices. Attachments copied from the game's MelonSlice (hand) and WaterMelonSlice_Ground
# (world, also used in hand by the dried slices) in scripts/generated/models_food.txt.
HAND = ["        attachment Bip01_Prop2", "        {", "            offset = -0.0242 0.0042 -0.0151,",
        "            rotate = -2.8745 40.3273 1.789,", "            scale = 0.6787,", "        }"]
WORLD = ["        attachment Bip01_Prop2", "        {", "            offset = -0.034 0.013 -0.028,",
         "            rotate = 93.0 -9.0 -33.0,", "        }"]


def write_models():
    m = ["module FoodDryingExtended", "{"]
    for n in [s[0] for s in SLICES]:
        m += [f"    model FDX_{n}Slice", "    {", "        mesh = MelonSlice,", f"        texture = FDX_{n}SliceHand,"]
        m += HAND + ["    }", ""]
        m += [f"    model FDX_{n}Slice_Ground", "    {", "        mesh = WorldItems/WaterMelonSlice,",
              f"        texture = WorldItems/FDX_{n}Slice,", "        scale = 0.4,"] + WORLD + ["    }", ""]
        m += [f"    model FDX_{n}SliceDried", "    {", "        mesh = WorldItems/FDX_FruitSliceDried,",
              f"        texture = WorldItems/FDX_{n}SliceDried,", "        scale = 0.4,"] + WORLD + ["    }", ""]
    m += ["}", ""]
    with open(os.path.join(ROOT, "FoodDryingExtended_models.txt"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(m))
    print(len(SLICES) * 3, "models written")


main()
