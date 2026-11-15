# Améliorations et idées

Ce document propose ; rien n'est implémenté sans validation.

## Améliorations de code

| ID | Problème | Fichier | Correction proposée | Priorité | Effort |
|---|---|---|---|---|---|
| C01 | `onTrayEmptied` retombe sur `getPlayer()` si `character` est nil ; sur un serveur dédié `getPlayer()` n'existe pas | `media/lua/shared/FoodDryingExtended.lua` (`onTrayEmptied`) | sortir sans rien donner si `character` est nil, avec un message console | basse | faible |
| C02 | Les deux fichiers copiés de Food Drying se resynchronisent à la main | `media/scripts/generated/...` | script `source/sync_food_drying.py` qui recopie et réapplique les modifications | moyenne | moyen |
| C03 | Tranches de fruits : rendu jamais vu en jeu | `textures/`, `models_X/` | capture en jeu automatique (PZDevKit) | moyenne | faible |

## Idées de fonctionnalités

| ID | Idée | Intérêt joueur | Faisabilité | Effort |
|---|---|---|---|---|
| I01 | Chips de pomme ou de banane | encas sucré | même plaque que les chips | faible |
| I02 | Tomates séchées à l'huile (bocal) | plats évolutifs | recette de bocal, dépend des règles `makeJar` | moyen |
| I03 | Viande séchée assaisonnée (jerky aux épices) | variété, moral | variante de la recette de Food Drying | moyen |
| I04 | Poudre de champignons séchés | assaisonnement | même modèle que F07 | faible |
| I05 | Thé de plantes sauvages séchées (orties, citronnelle) | boisson, moral | recette de boisson vanilla à étudier | moyen |
| I06 | Mélange montagnard (fruits secs + noix + graines) | ration de voyage | recette simple, nutrition additionnée | faible |
| I07 | Sac en papier pour les roulés de fruits | conservation | même mécanisme que F08 | faible |
| I08 | Graines de citrouille grillées | encas, déchet valorisé | plaque du mod | faible |
| I09 | Algues ou poissons séchés au sel sur le séchoir | côte | mappers du séchoir | moyen |
| I10 | Magazine « Séchage maison » qui débloque les recettes du mod | apprentissage | objet littérature | faible |
