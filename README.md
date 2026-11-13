# Food Drying Extended

Extension of [Food Drying [B42]](https://steamcommunity.com/sharedfiles/filedetails/?id=3747396551) by Corvus, for Project Zomboid Build 42.21.

- Mod id: `batman_FoodDryingExtended` (requires `FoodDrying`, loads after `FoodDrying_VFEPatch` when present)
- New dried vegetables: Brussels sprouts, cucumber, pumpkin, sweet potato, turnip, zucchini (oven tray, skewer, drying rack)
- Homemade crisps: potato tray baked in the oven, one portion per potato, optional paper bag

## How it plugs into Food Drying

| Part | Mechanism | File |
|---|---|---|
| Trays and skewers | vanilla vegetables get the `fooddrying:dryablevegetable` tag (tags add up, other mods' tags stay) | `media/scripts/FoodDryingExtended_vanilla_overrides.txt` |
| Raw to dried item | entries added to `OvenDrying.dryableTypes` (public table of Food Drying) | `media/lua/shared/FoodDryingExtended.lua` |
| Drying rack | copy of Food Drying's rack recipes file, same relative path, with 6 more lines in the `DryVegetables` mapper | `media/scripts/generated/entities/agricultural/workstations/entity_Food_Drying_Rack_craftRecipe.txt` |
| Shelf life option | dried vegetables carry `fooddrying:driedvegetables`, so Food Drying's multiplier applies | `media/scripts/FoodDryingExtended_items.txt` |
| Crisps | own tray, empty and bag recipes, reusing `OvenDrying.onContainerFilled` / `onContainerEmptied` | `media/scripts/FoodDryingExtended_recipes.txt` |

## Updating after a Food Drying update

The rack recipes file replaces Food Drying's own. When Food Drying changes `entity_Food_Drying_Rack_craftRecipe.txt`, copy the new file and add the six `FoodDryingExtended.*Dried` lines back at the end of the `itemMapper vegetables` block.

`source/make_poster.py` rebuilds the poster from the original Food Drying artwork (Pillow); `preview.png` is the poster resized to 256 px.

## Credits

Food Drying, its rack recipes file and its artwork are made by Corvus; all rights to the original mod belong to its author.
