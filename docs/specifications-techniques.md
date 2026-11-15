# Spécifications techniques

Cible : Build 42.21 et 42.22 (variante `42.21/`). Dépendance : `require=\FoodDrying`, chargé après `FoodDrying` et `FoodDrying_VFEPatch`.

## Objets (module `FoodDryingExtended`, 50)

| Groupe | Objets |
|---|---|
| Légumes séchés | `BrusselSproutsDried`, `CucumberDried`, `SweetPotatoDried`, `TurnipDried`, `ZucchiniDried`, `CabbageDried`, `SugarBeetDried`, `GarlicDried`, `GreenOnionsDried`, `PumpkinSlicedDried` |
| Tranches de fruits | `PineappleSlice`, `MangoSlice`, `GrapefruitSlice` et leurs `...Dried` ; `WatermelonDried`, `RosehipsDried` |
| Plantes sauvages | `DandelionsDried`, `GingerRootDried`, `GrapeLeavesDried`, `VioletsDried`, `ThistleDried`, `NettlesDried`, `LemonGrassDried`, `GinsengDried` |
| Fruits de mer | `ShrimpSalted`, `ShrimpDried`, `SquidSalted`, `SquidDried`, `CrayfishSalted`, `CrayfishDried`, `OystersSalted`, `OystersDried` |
| Plaques | `BakingTrayCrisps`, `BakingTrayCrispsOil`, `BakingTrayFruitLeather`, `BakingTrayInsects` |
| Produits des plaques | `HomemadeCrisps`, `SweetPotatoCrisps`, `SugarBeetCrisps`, `ZucchiniCrisps`, `KaleCrisps`, `HomemadeCrispsBag`, `FruitLeather`, `RoastedCricket`, `RoastedGrasshopper`, `RoastedSawflyLarva`, `RoastedCaterpillar` |
| Pemmican | `Pemmican` (365 jours frais, 730 avant pourriture) |

Les objets séchés portent les tags `fooddrying:dried*` de Food Drying. Modèles : 10 entrées dans `FoodDryingExtended_models.txt`.

## Objets vanilla modifiés

`FoodDryingExtended_vanilla_overrides.txt` ajoute un tag `fooddrying:dryable*` à 22 objets vanilla (les tags s'additionnent). `VanillaFruitOverrides.txt` (copie du fichier de Food Drying) retire `fooddrying:dryablefruit` de `Grapefruit`, `Mango` et `Pineapple`.

## Recettes (module `FoodDryingExtended`)

| Recette | Rôle | Fonctions |
|---|---|---|
| `SliceLargeFruit` | gros fruit → 4 tranches | — |
| `PrepareHomemadeCrispsTray`, `PrepareHomemadeCrispsTrayOil`, `PrepareFruitLeatherTray`, `PrepareRoastedInsectsTray` | remplir une plaque | OnTest `FoodDrying.OvenDryingTest`, OnCreate `FoodDryingExtended.onTrayFilled` |
| `EmptyExtendedTray` | vider une plaque du mod | OnCreate `FoodDryingExtended.onTrayEmptied` |
| `BagHomemadeCrisps` | chips → sac en papier | OnTest `FoodDryingExtended.isEmptyPaperBag`, OnCreate `FoodDryingExtended.onCrispsBagged` |
| `SaltSeafood` | fruit de mer + 5 sel → fruit de mer salé (`InheritFood`) | — |
| `DryWildPlants` | séchoir à herbes vanilla, 1 à 20 plantes | OnCreate `FoodDrying.DryingRack_OnCreate` |
| `GrindBasilSeasoning` … `GrindThymeSeasoning` (8) | 4 herbes séchées → assaisonnement vanilla | — |
| `MakePemmican`, `MakePemmicanWithBerries` | 1 à 4 viandes séchées + 6 doses de saindoux ou beurre (+ 1 à 4 baies séchées) → barres de pemmican | OnCreate `FoodDryingExtended.onPemmicanMade` |

Séchoir de Food Drying : mappers `fruit`, `berries`, `fish`, `vegetables` complétés dans la copie de `entity_Food_Drying_Rack_craftRecipe.txt`.

## ModData des plaques

Clé `fdxEntries` sur la plaque : tableau d'entrées, une par aliment consommé accepté.

| Champ | Contenu |
|---|---|
| `rawType` | type complet de l'aliment cru |
| `hunger`, `calories`, `carbohydrates`, `lipids`, `proteins`, `unhappy` | valeurs de l'aliment au remplissage |
| `agedRatio` | âge / `OffAgeMax` (0 si non périssable) |
| `poisonPower`, `poisonDetection` | poison de l'aliment |

Au vidage : plaque non cuite → aliments crus rendus ; `pooled` → `max(1, faim totale / 12)` roulés, nutrition partagée ; sinon un produit cuit par entrée (bonus d'huile ajouté si `oil`).

## Pemmican

`onPemmicanMade` additionne la nutrition des aliments consommés (hors gras) et celle de 6 doses d'un bloc neuf du gras utilisé, puis fait `max(1, arrondi(faim totale / 20))` barres, nutrition partagée ; le poison le plus fort est reporté sur chaque barre. Les barres en plus vont dans l'inventaire du personnage (une seule barre si la fonction est appelée sans personnage).

## Traductions

EN, FR, DE, ES, PT, PTBR, RU, CN, JP, KO, TR : `ItemName.json` (`FoodDryingExtended.<Objet>`) et `Recipes.json`. Les noms français des objets du mod vivent ici, pas dans Food Drying FR.

## Compatibilité

- Food Drying VFE Patch : chargé avant (`loadModAfter`).
- DryThatFood : pas de conflit, séchage de fruits et légumes en double.
- Les deux fichiers remplacés doivent suivre les versions de Food Drying (voir [developpement.md](developpement.md)).
