# Food Drying Extended

Extension of [Food Drying [B42]](https://steamcommunity.com/sharedfiles/filedetails/?id=3747396551) by Corvus, for Project Zomboid Build 42.21.

- Mod id: `batman_FoodDryingExtended` (requires `FoodDrying`, loads after `FoodDrying_VFEPatch` when present)
- More food to dry (oven tray, skewer, drying rack): Brussels sprouts, cucumber, pumpkin slices, sweet potato, turnip, zucchini, cabbage, sugar beet, garlic, green onions, slices of watermelon, pineapple, mango and grapefruit (Slice Large Fruit recipe), rose hips; jalapeño and habanero in the oven and on skewers
- Seafood: Salt Seafood (shrimp, squid, crayfish, oysters), then the drying rack
- Wild plants (herb drying rack, oven, skewer): dandelions, ginger root, grape leaves, violets, thistles, nettles, lemongrass, ginseng; grinding of 8 vanilla dried herbs into vanilla seasonings (mortar and pestle)
- Own oven trays: homemade crisps (5 vegetables, with or without oil, optional paper bag), fruit leather, roasted insects
- Languages: EN, FR, DE, ES, PT, PTBR, RU, CN, JP, KO, TR

## How it plugs into Food Drying

| Part | Mechanism | File |
|---|---|---|
| Trays and skewers of Food Drying | vanilla items get the `fooddrying:dryable*` tags (tags add up, other mods' tags stay) | `media/scripts/FoodDryingExtended_vanilla_overrides.txt` |
| Raw to dried item | entries added to `OvenDrying.dryableTypes` (public table of Food Drying) | `media/lua/shared/FoodDryingExtended.lua` |
| Drying rack | copy of Food Drying's rack recipes file, same relative path, with 26 more mapper lines (fruit, berries, vegetables, fish) | `media/scripts/generated/entities/agricultural/workstations/entity_Food_Drying_Rack_craftRecipe.txt` |
| Large fruits | copy of Food Drying's fruit tags file without the dryable tag on whole pineapple, mango and grapefruit (a tag cannot be removed otherwise), plus `SliceLargeFruit` and slice items | `media/scripts/generated/items/VanillaFruitOverrides.txt`, `FoodDryingExtended_recipes.txt` |
| Shelf life option | dried items carry `fooddrying:dried*`, so Food Drying's multiplier applies | `media/scripts/FoodDryingExtended_items.txt` |
| Own trays | `FoodDryingExtended.onTrayFilled` stores one entry per food in the tray's ModData, `onTrayEmptied` gives the cooked (or raw) food back | `media/scripts/FoodDryingExtended_recipes.txt`, `FoodDryingExtended.lua` |
| Seafood salting | own `SaltSeafood` recipe (not Food Drying's `SaltMeatAndFish`, whose mapper would accept the tag but give nothing) | `FoodDryingExtended_recipes.txt` |

Items, translations and Steam descriptions are generated: edit `source/build_scripts.py`, `source/build_translations.py` or `source/build_descriptions.py` (11 languages, recipe table with names read from `Recipes.json`), then run them.

## Tests

Offline checks (references, translations, tray logic in lupa): `python tests/run_tests.py`.

In-game automated test with PZDevKit: `python PZDevKit/pzdev.py sp FoodDryingExtended --wait-idle 3600` (from the Workshop folder; hooks in `autotest/fdx_hooks.lua`).

## Updating after a Food Drying update

Two files replace Food Drying's own. When Food Drying changes `VanillaFruitOverrides.txt`, copy the new file and remove `fooddrying:dryablefruit` from the `Tags` of Grapefruit, Mango and Pineapple. When it changes `entity_Food_Drying_Rack_craftRecipe.txt`, copy the new file, replace the Pineapple, Mango and Grapefruit lines of the `fruit` mapper by the slice lines and add back the `FoodDryingExtended.*` and `Base.Pepper*Dried` lines at the end of the `fruit`, `berries`, `fish` and `vegetables` item mappers, then run the in-game test.

`source/make_poster.py` rebuilds the poster from the original Food Drying artwork (Pillow); `preview.png` is the poster resized to 256 px.

## Credits

Food Drying, its rack recipes file and its artwork are made by Corvus; all rights to the original mod belong to its author.
