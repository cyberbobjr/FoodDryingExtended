# Architecture

## Vue d'ensemble

Le mod ne réécrit pas Food Drying : il s'y branche par ses points publics (tags `fooddrying:*`, table `OvenDrying.dryableTypes`, fonctions `FoodDrying.OvenDryingTest` et `FoodDrying.DryingRack_OnCreate`) et remplace deux fichiers de scripts que Food Drying n'offre pas autrement d'étendre.

## Arborescence

```
Contents/mods/batman_FoodDryingExtended/
├── common/                      vide (.gitkeep), exigé par la structure Build 42
└── 42.21/                       variante chargée en 42.21 et 42.22
    ├── mod.info                 require=\FoodDrying, loadModAfter=FoodDrying,FoodDrying_VFEPatch
    ├── poster.png
    └── media/
        ├── lua/shared/FoodDryingExtended.lua            enregistrement four/brochette, plaques du mod, sac de chips, pemmican
        ├── lua/shared/Translate/<LANGUE>/ItemName.json, Recipes.json   11 langues
        ├── scripts/FoodDryingExtended_items.txt         50 objets, module FoodDryingExtended
        ├── scripts/FoodDryingExtended_recipes.txt       recettes du mod
        ├── scripts/FoodDryingExtended_models.txt        modèles des tranches de fruits et du pemmican
        ├── scripts/FoodDryingExtended_vanilla_overrides.txt   tags fooddrying:* ajoutés à 22 objets vanilla
        ├── scripts/generated/entities/agricultural/workstations/entity_Food_Drying_Rack_craftRecipe.txt   copie modifiée (Food Drying)
        ├── scripts/generated/items/VanillaFruitOverrides.txt   copie modifiée (Food Drying)
        ├── models_X/WorldItems/FDX_FruitSliceDried.fbx, FDX_Pemmican.fbx
        └── textures/                                    icônes et textures des tranches et du pemmican
```

## Branchement sur Food Drying

| Partie | Mécanisme | Fichier |
|---|---|---|
| Plaques et brochettes de Food Drying | les objets vanilla reçoivent les tags `fooddrying:dryable*` (les tags s'additionnent, ceux des autres mods restent) | `FoodDryingExtended_vanilla_overrides.txt` |
| Objet cru → objet séché | entrées ajoutées à `OvenDrying.dryableTypes`, seulement si les deux scripts existent (sinon message `FOODDRYINGEXTENDED WARNING`) | `FoodDryingExtended.lua` |
| Séchoir | copie du fichier de recettes du séchoir de Food Drying, même chemin relatif, avec les lignes de mapper du mod (fruits, baies, légumes, poisson) | `entity_Food_Drying_Rack_craftRecipe.txt` |
| Gros fruits | copie du fichier de tags fruits de Food Drying sans le tag séchable sur ananas, mangue et pamplemousse entiers (un tag ne peut pas se retirer autrement), plus `SliceLargeFruit` | `VanillaFruitOverrides.txt`, `FoodDryingExtended_recipes.txt` |
| Option de durée de conservation | les objets séchés portent `fooddrying:dried*`, donc le multiplicateur de Food Drying s'applique | `FoodDryingExtended_items.txt` |
| Plaques du mod | `onTrayFilled` mémorise une entrée par aliment dans la ModData de la plaque, `onTrayEmptied` rend l'aliment cuit (ou cru) | `FoodDryingExtended.lua` |
| Fruits de mer salés | recette propre `SaltSeafood` (le mapper de `SaltMeatAndFish` de Food Drying accepterait le tag sans rien donner) | `FoodDryingExtended_recipes.txt` |

## Lua (`media/lua/shared/FoodDryingExtended.lua`)

- `require "OvenDrying"` (Food Drying), puis remplissage de `OvenDrying.dryableTypes`.
- `FoodDryingExtended.TRAYS` : type de plaque → règle (`map` cru → cuit, `pooled` pour les roulés, `oil` pour le bonus d'huile, `cookedModel`).
- `onTrayFilled` (OnCreate des recettes `Prepare...Tray`), `onTrayEmptied` (OnCreate de `EmptyExtendedTray`), `onTrayCooked` (OnCooked des plaques), `isEmptyPaperBag` (OnTest de `BagHomemadeCrisps`), `onCrispsBagged` (OnCreate de `BagHomemadeCrisps`), `onPemmicanMade` (OnCreate de `MakePemmican` et `MakePemmicanWithBerries`).
- Constantes : `OIL_CALORIES = 70`, `OIL_LIPIDS = 8`, `OIL_UNHAPPY = -10`, `LEATHER_HUNGER_PER_ROLL = 12`, `PEMMICAN_HUNGER_PER_BAR = 20`, `PEMMICAN_FAT_USES = 6`, `PEMMICAN_FATS` (saindoux, beurre).

Aucun événement, aucune commande réseau : tout passe par les recettes, exécutées par le serveur en multijoueur.

## Persistance

`fdxEntries` dans la ModData de chaque plaque du mod : liste d'entrées (voir [specifications-techniques.md](specifications-techniques.md#moddata-des-plaques)).

## Outillage et tests

| Commande | Effet |
|---|---|
| `python source/build_scripts.py` | génère objets, recettes et modèles |
| `python source/build_translations.py` | génère les traductions, 11 langues |
| `python source/build_descriptions.py` | génère `README.steam*` et la description de `workshop.txt` (tableau des recettes) |
| `python source/make_poster.py` | refait le poster depuis l'illustration de Food Drying (Pillow) ; `preview.png` = poster en 256 px |
| `source/slices/recolor_textures.py`, `thin_slice_mesh.py`, `render_slices.py` | textures, maillage aminci et icônes 64 px des tranches de fruits (Blender) |
| `source/pemmican/make_texture.py`, `build_pemmican.py` | texture, modèle et icône de la barre de pemmican (maillage de la barre de céréales du jeu, Blender) |
| `python tests/run_tests.py` | contrôles hors ligne : références, traductions, logique des plaques sous lupa |
| `python PZDevKit/pzdev.py sp FoodDryingExtended --wait-idle 3600` | test en jeu automatique (depuis `Workshop`), crochets `autotest/fdx_hooks.lua` |
