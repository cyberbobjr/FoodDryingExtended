# Développement — contraintes du projet

## Périmètre

Un seul mod : `batman_FoodDryingExtended`, `require=\FoodDrying` (Workshop 3747396551, Corvus). Food Drying, son fichier de recettes du séchoir et son illustration appartiennent à leur auteur.

## Fichiers générés

Objets, recettes, modèles, traductions et descriptions Steam sont générés par `source/build_*.py` : modifier le générateur, puis le relancer, jamais le fichier produit.

## Après une mise à jour de Food Drying

Deux fichiers remplacent ceux de Food Drying (même chemin relatif) :

1. **`media/scripts/generated/items/VanillaFruitOverrides.txt`** : recopier le nouveau fichier de Food Drying, puis retirer `fooddrying:dryablefruit` des `Tags` de `Grapefruit`, `Mango` et `Pineapple`.
2. **`media/scripts/generated/entities/agricultural/workstations/entity_Food_Drying_Rack_craftRecipe.txt`** : recopier le nouveau fichier, remplacer les lignes `Pineapple`, `Mango` et `Grapefruit` du mapper `fruit` par les lignes des tranches, puis rajouter les lignes `FoodDryingExtended.*` et `Base.Pepper*Dried` à la fin des mappers `fruit`, `berries`, `fish` et `vegetables`.

Ensuite : `python tests/run_tests.py`, puis le test en jeu (`python PZDevKit/pzdev.py sp FoodDryingExtended --wait-idle 3600` depuis `Workshop`).
