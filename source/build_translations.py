"""Writes the translation files of Food Drying Extended (ItemName.json, Recipes.json)
for every language of the tables below.

Usage: python source/build_translations.py
Item names follow the vanilla vocabulary of each language (media/lua/shared/Translate/<LANG>/ItemName.json).
"""
import json
import os

ROOT = os.path.join(os.path.dirname(__file__), "..", "Contents", "mods", "batman_FoodDryingExtended",
                    "42.21", "media", "lua", "shared", "Translate")

ITEMS = ["BrusselSproutsDried", "CucumberDried", "PumpkinSlicedDried", "SweetPotatoDried", "TurnipDried", "ZucchiniDried",
         "CabbageDried", "SugarBeetDried", "GarlicDried", "GreenOnionsDried", "WatermelonDried", "RosehipsDried",
         "ShrimpSalted", "ShrimpDried", "SquidSalted", "SquidDried", "CrayfishSalted", "CrayfishDried",
         "OystersSalted", "OystersDried",
         "BakingTrayCrisps", "BakingTrayCrispsOil", "BakingTrayFruitLeather", "BakingTrayInsects",
         "HomemadeCrisps", "SweetPotatoCrisps", "SugarBeetCrisps", "ZucchiniCrisps", "KaleCrisps", "HomemadeCrispsBag",
         "FruitLeather", "RoastedCricket", "RoastedGrasshopper", "RoastedSawflyLarva", "RoastedCaterpillar"]

RECIPES = ["PrepareHomemadeCrispsTray", "PrepareHomemadeCrispsTrayOil", "PrepareFruitLeatherTray",
           "PrepareRoastedInsectsTray", "EmptyExtendedTray", "BagHomemadeCrisps", "SaltSeafood"]

T = {
    "EN": (
        ["Dried Brussels Sprouts", "Dried Cucumber", "Dried Pumpkin Slice", "Dried Sweet Potato", "Dried Turnip", "Dried Zucchini",
         "Dried Cabbage", "Dried Sugar Beet", "Dried Garlic", "Dried Green Onions", "Dried Watermelon", "Dried Rose Hips",
         "Salted Shrimp", "Dried Shrimp", "Salted Squid", "Dried Squid", "Salted Crayfish", "Dried Crayfish",
         "Salted Oysters", "Dried Oysters",
         "Baking Tray with Sliced Vegetables", "Baking Tray with Oiled Sliced Vegetables", "Baking Tray with Fruit Puree",
         "Baking Tray with Insects",
         "Homemade Potato Crisps", "Sweet Potato Crisps", "Beet Crisps", "Zucchini Crisps", "Kale Crisps",
         "Bag of Homemade Crisps",
         "Fruit Leather", "Roasted Cricket", "Roasted Grasshopper", "Roasted Sawfly Larva", "Roasted Caterpillar"],
        ["Prepare a Tray of Homemade Crisps", "Prepare a Tray of Crisps with Oil", "Prepare a Tray of Fruit Leather",
         "Prepare a Tray of Insects to Roast", "Empty the Baking Tray", "Put Homemade Crisps in a Paper Bag",
         "Salt Seafood"]),
    "FR": (
        ["Choux de Bruxelles séchés", "Concombre séché", "Tranche de citrouille séchée", "Patate douce séchée", "Navet séché",
         "Courgette séchée", "Chou séché", "Betterave sucrière séchée", "Ail séché", "Cébettes séchées",
         "Pastèque séchée", "Églantier séché",
         "Crevette salée", "Crevette séchée", "Calmar salé", "Calmar séché", "Écrevisse salée", "Écrevisse séchée",
         "Huîtres salées", "Huîtres séchées",
         "Plaque de cuisson avec légumes en tranches", "Plaque de cuisson avec légumes en tranches à l'huile",
         "Plaque de cuisson avec purée de fruits", "Plaque de cuisson avec insectes",
         "Chips maison", "Chips de patate douce", "Chips de betterave", "Chips de courgette", "Chips de chou frisé",
         "Sachet de chips maison",
         "Roulé de fruits séchés", "Criquet grillé", "Sauterelle grillée", "Larve de tenthrède grillée", "Chenille grillée"],
        ["Préparer une plaque de chips maison", "Préparer une plaque de chips à l'huile",
         "Préparer une plaque de roulés de fruits", "Préparer une plaque d'insectes à griller",
         "Vider la plaque de cuisson", "Mettre des chips maison en sachet", "Saler des fruits de mer"]),
    "DE": (
        ["Getrockneter Rosenkohl", "Getrocknete Gurke", "Getrocknete Kürbisscheibe", "Getrocknete Süßkartoffel",
         "Getrocknete Rübe", "Getrocknete Zucchini", "Getrockneter Kohlkopf", "Getrocknete Zuckerrübe",
         "Getrockneter Knoblauch", "Getrocknete grüne Zwiebeln", "Getrocknete Wassermelone", "Getrocknete Hagebutten",
         "Gesalzene Shrimps", "Getrocknete Shrimps", "Gesalzener Tintenfisch", "Getrockneter Tintenfisch",
         "Gesalzener Flusskrebs", "Getrockneter Flusskrebs", "Gesalzene Austern", "Getrocknete Austern",
         "Backblech mit Gemüsescheiben", "Backblech mit geölten Gemüsescheiben", "Backblech mit Fruchtpüree",
         "Backblech mit Insekten",
         "Hausgemachte Kartoffelchips", "Süßkartoffelchips", "Rübenchips", "Zucchinichips", "Grünkohlchips",
         "Tüte hausgemachter Chips",
         "Fruchtleder", "Geröstete Grille", "Gerösteter Grashüpfer", "Geröstete Blattwespen-Larve", "Geröstete Raupe"],
        ["Backblech mit hausgemachten Chips vorbereiten", "Backblech mit Chips in Öl vorbereiten",
         "Backblech mit Fruchtleder vorbereiten", "Backblech mit Insekten zum Rösten vorbereiten",
         "Backblech leeren", "Hausgemachte Chips in eine Papiertüte füllen", "Meeresfrüchte salzen"]),
    "ES": (
        ["Coles de Bruselas secas", "Pepino seco", "Calabaza cortada seca", "Boniato seco", "Nabo seco", "Calabacín seco",
         "Col seca", "Remolacha azucarera seca", "Ajo seco", "Cebollines secos", "Sandía seca", "Escaramujos secos",
         "Gamba salada", "Gamba seca", "Calamar salado", "Calamar seco", "Cangrejo de río salado",
         "Cangrejo de río seco", "Ostras saladas", "Ostras secas",
         "Bandeja de horno con verduras en rodajas", "Bandeja de horno con verduras en rodajas con aceite",
         "Bandeja de horno con puré de fruta", "Bandeja de horno con insectos",
         "Patatas fritas caseras", "Chips de boniato", "Chips de remolacha", "Chips de calabacín", "Chips de col rizada",
         "Bolsa de patatas fritas caseras",
         "Lámina de fruta", "Grillo tostado", "Saltamontes tostado", "Larva de mosca de sierra tostada", "Oruga tostada"],
        ["Preparar una bandeja de patatas fritas caseras", "Preparar una bandeja de patatas fritas con aceite",
         "Preparar una bandeja de láminas de fruta", "Preparar una bandeja de insectos para tostar",
         "Vaciar la bandeja de horno", "Meter patatas fritas caseras en una bolsa de papel", "Salar marisco"]),
    "PT": (
        ["Couves-de-bruxelas secas", "Pepino seco", "Fatia de Abóbora seca", "Batata-doce seca", "Nabo seco", "Curgete seca",
         "Couve seca", "Beterraba seca", "Alho seco", "Cebolinha seca", "Melancia seca", "Rosa mosqueta seca",
         "Camarão salgado", "Camarão seco", "Lula salgada", "Lula seca", "Lagostim salgado", "Lagostim seco",
         "Ostras salgadas", "Ostras secas",
         "Tabuleiro de forno com legumes fatiados", "Tabuleiro de forno com legumes fatiados em óleo",
         "Tabuleiro de forno com puré de fruta", "Tabuleiro de forno com insetos",
         "Batatas fritas caseiras", "Chips de batata-doce", "Chips de beterraba", "Chips de curgete",
         "Chips de couve frisada", "Saco de batatas fritas caseiras",
         "Rolo de fruta seca", "Grilo torrado", "Gafanhoto torrado", "Larva de vespa-serra torrada", "Lagarta torrada"],
        ["Preparar um tabuleiro de batatas fritas caseiras", "Preparar um tabuleiro de batatas fritas com óleo",
         "Preparar um tabuleiro de rolos de fruta", "Preparar um tabuleiro de insetos para torrar",
         "Esvaziar o tabuleiro de forno", "Pôr batatas fritas caseiras num saco de papel", "Salgar marisco"]),
    "PTBR": (
        ["Couve-de-Bruxelas Seca", "Pepino Seco", "Fatia de Abóbora Seca", "Batata-doce Seca", "Nabo Seco", "Abobrinha Seca",
         "Repolho Seco", "Beterraba Doce Seca", "Alho Seco", "Cebolinha Verde Seca", "Melancia Seca",
         "Frutos de Rosa-mosqueta Secos",
         "Camarão Salgado", "Camarão Seco", "Lula Salgada", "Lula Seca", "Lagostim Salgado", "Lagostim Seco",
         "Ostras Salgadas", "Ostras Secas",
         "Assadeira com Legumes Fatiados", "Assadeira com Legumes Fatiados no Óleo", "Assadeira com Purê de Frutas",
         "Assadeira com Insetos",
         "Batata Chips Caseira", "Chips de Batata-doce", "Chips de Beterraba", "Chips de Abobrinha", "Chips de Couve",
         "Saquinho de Chips Caseiros",
         "Rolinho de Fruta Desidratada", "Grilo Torrado", "Gafanhoto Torrado", "Larva de Vespa-serra Torrada",
         "Lagarta Torrada"],
        ["Preparar Assadeira de Batata Chips Caseira", "Preparar Assadeira de Chips com Óleo",
         "Preparar Assadeira de Rolinhos de Fruta", "Preparar Assadeira de Insetos para Torrar",
         "Esvaziar a Assadeira", "Colocar Chips Caseiros em um Saco de Papel", "Salgar Frutos do Mar"]),
    "RU": (
        ["Сушёная брюссельская капуста", "Сушёный огурец", "Сушёные ломтики тыквы", "Сушёный батат", "Сушёная репа",
         "Сушёные цуккини", "Сушёная капуста", "Сушёная сахарная свёкла", "Сушёный чеснок", "Сушёный зелёный лук",
         "Сушёный арбуз", "Сушёные плоды шиповника",
         "Солёная креветка", "Сушёная креветка", "Солёный кальмар", "Сушёный кальмар", "Солёный речной рак",
         "Сушёный речной рак", "Солёные устрицы", "Сушёные устрицы",
         "Противень с нарезанными овощами", "Противень с нарезанными овощами в масле", "Противень с фруктовым пюре",
         "Противень с насекомыми",
         "Домашние картофельные чипсы", "Чипсы из батата", "Чипсы из свёклы", "Чипсы из цуккини",
         "Чипсы из кудрявой капусты", "Пакет домашних чипсов",
         "Фруктовая пастила", "Жареный сверчок", "Жареный кузнечик", "Жареная личинка пилильщика", "Жареная гусеница"],
        ["Приготовить противень домашних чипсов", "Приготовить противень чипсов на масле",
         "Приготовить противень фруктовой пастилы", "Приготовить противень насекомых для обжарки",
         "Освободить противень", "Положить домашние чипсы в бумажный пакет", "Засолить морепродукты"]),
    "CN": (
        ["干孢子甘蓝", "干黄瓜", "南瓜片干", "红薯干", "干芜菁", "西葫芦干", "干卷心菜", "甜菜干", "干大蒜", "干青葱",
         "西瓜干", "干玫瑰果",
         "咸虾", "虾干", "咸鱿鱼", "鱿鱼干", "咸小龙虾", "小龙虾干", "咸牡蛎", "牡蛎干",
         "放有蔬菜片的烘烤板", "放有油拌蔬菜片的烘烤板", "放有果泥的烘烤板", "放有昆虫的烘烤板",
         "自制薯片", "红薯片", "甜菜片", "西葫芦片", "羽衣甘蓝脆片", "一袋自制薯片",
         "果丹皮", "烤蟋蟀", "烤蚱蜢", "烤叶蜂幼虫", "烤毛毛虫"],
        ["准备一板自制薯片", "准备一板油炸薯片", "准备一板果丹皮", "准备一板待烤昆虫", "清空烘烤板",
         "把自制薯片装进纸袋", "腌制海鲜"]),
    "JP": (
        ["乾燥メキャベツ", "乾燥キュウリ", "乾燥カボチャのカット", "干し芋", "乾燥カブ", "乾燥ズッキーニ", "乾燥キャベツ",
         "乾燥テンサイ", "乾燥ニンニク", "乾燥ネギ", "乾燥スイカ", "乾燥ローズヒップ",
         "塩漬けエビ", "干しエビ", "塩漬けイカ", "干しイカ", "塩漬けザリガニ", "干しザリガニ", "塩漬けカキ", "干しカキ",
         "スライス野菜のベーキングトレイ", "油をまぶしたスライス野菜のベーキングトレイ",
         "フルーツピューレのベーキングトレイ", "昆虫のベーキングトレイ",
         "自家製ポテトチップス", "サツマイモチップス", "テンサイチップス", "ズッキーニチップス", "ケールチップス",
         "自家製チップスの袋",
         "フルーツレザー", "コオロギのロースト", "バッタのロースト", "ハバチ幼虫のロースト", "イモムシのロースト"],
        ["自家製ポテトチップスのトレイを準備", "油を使ったチップスのトレイを準備", "フルーツレザーのトレイを準備",
         "ロースト用の昆虫のトレイを準備", "ベーキングトレイを空にする", "自家製チップスを紙袋に入れる",
         "魚介類を塩漬けにする"]),
    "KO": (
        ["말린 방울양배추", "말린 오이", "말린 호박 조각", "말린 고구마", "말린 순무", "말린 애호박", "말린 양배추",
         "말린 사탕무", "말린 마늘", "말린 파", "말린 수박", "말린 로즈힙",
         "소금에 절인 새우", "말린 새우", "소금에 절인 오징어", "말린 오징어", "소금에 절인 가재", "말린 가재",
         "소금에 절인 굴", "말린 굴",
         "썬 채소를 올린 제빵 쟁반", "기름을 두른 썬 채소를 올린 제빵 쟁반", "과일 퓌레를 올린 제빵 쟁반",
         "곤충을 올린 제빵 쟁반",
         "수제 감자칩", "고구마칩", "사탕무칩", "애호박칩", "케일칩", "수제 감자칩 봉투",
         "과일 레더", "구운 귀뚜라미", "구운 메뚜기", "구운 잎벌 유충", "구운 애벌레"],
        ["수제 감자칩 쟁반 준비", "기름 감자칩 쟁반 준비", "과일 레더 쟁반 준비", "구울 곤충 쟁반 준비",
         "제빵 쟁반 비우기", "수제 감자칩을 종이 봉투에 담기", "해산물 소금에 절이기"]),
    "TR": (
        ["Kurutulmuş Brüksel Lahanası", "Kurutulmuş Salatalık", "Kurutulmuş Balkabağı Dilimi", "Kurutulmuş Tatlı Patates",
         "Kurutulmuş Şalgam", "Kurutulmuş Kabak", "Kurutulmuş Lahana", "Kurutulmuş Şeker Pancarı",
         "Kurutulmuş Sarımsak", "Kurutulmuş Taze Soğan", "Kurutulmuş Karpuz", "Kurutulmuş Kuşburnu",
         "Tuzlanmış Karides", "Kurutulmuş Karides", "Tuzlanmış Kalamar", "Kurutulmuş Kalamar", "Tuzlanmış Kerevit",
         "Kurutulmuş Kerevit", "Tuzlanmış İstiridye", "Kurutulmuş İstiridye",
         "Dilimlenmiş Sebzeli Fırın Tepsisi", "Yağlı Dilimlenmiş Sebzeli Fırın Tepsisi", "Meyve Püreli Fırın Tepsisi",
         "Böcekli Fırın Tepsisi",
         "Ev Yapımı Patates Cipsi", "Tatlı Patates Cipsi", "Pancar Cipsi", "Kabak Cipsi", "Kara Lahana Cipsi",
         "Ev Yapımı Cips Paketi",
         "Meyve Pestili", "Kavrulmuş Cırcır Böceği", "Kavrulmuş Çekirge", "Kavrulmuş Testereli Arı Larvası",
         "Kavrulmuş Tırtıl"],
        ["Bir Tepsi Ev Yapımı Cips Hazırla", "Bir Tepsi Yağlı Cips Hazırla", "Bir Tepsi Meyve Pestili Hazırla",
         "Kavurmak İçin Bir Tepsi Böcek Hazırla", "Fırın Tepsisini Boşalt", "Ev Yapımı Cipsi Kese Kağıdına Koy",
         "Deniz Ürünlerini Tuzla"]),
}


# Wild plants (vanilla "Herb (Dried)" naming), the herb rack recipe and the grinding recipes
# (one recipe per herb, all with the same label).
WILD_ITEMS = ["DandelionsDried", "GingerRootDried", "GrapeLeavesDried", "VioletsDried", "ThistleDried",
              "NettlesDried", "LemonGrassDried", "GinsengDried"]
HERBS = ["Basil", "Chives", "Cilantro", "Oregano", "Parsley", "Rosemary", "Sage", "Thyme"]
WILD_T = {
    "EN": (["Dandelions (Dried)", "Ginger Root (Dried)", "Grape Leaves (Dried)", "Violets (Dried)", "Thistles (Dried)",
            "Nettles (Dried)", "Lemongrass (Dried)", "Ginseng (Dried)"], "Dry Wild Plants", "Grind into Seasoning"),
    "FR": (["Pissenlits (séchés)", "Racine de gingembre (séchée)", "Feuilles de vigne (séchées)", "Violettes (séchées)",
            "Chardon (séché)", "Orties (séchées)", "Citronnelle (séchée)", "Ginseng (séché)"],
           "Sécher des plantes sauvages", "Moudre en épice"),
    "DE": (["Löwenzahn (getrocknet)", "Ingwer (getrocknet)", "Weinblätter (getrocknet)", "Veilchen (getrocknet)",
            "Distel (getrocknet)", "Brennnesseln (getrocknet)", "Zitronengras (getrocknet)", "Ginseng (getrocknet)"],
           "Wildpflanzen trocknen", "Zu Gewürz mahlen"),
    "ES": (["Dientes de león (Secos)", "Jengibre (Seco)", "Hojas de parra (Secas)", "Violetas (Secas)",
            "Cardos (Secos)", "Ortigas (Secas)", "Citronela (Seca)", "Ginseng (Seco)"],
           "Secar plantas silvestres", "Moler como especia"),
    "PT": (["Dentes-de-leão (Secos)", "Raiz de Gengibre (Seca)", "Folhas de Uva (Secas)", "Violetas (Secas)",
            "Cardos (Secos)", "Urtigas (Secas)", "Citronela (Seca)", "Ginseng (Seco)"],
           "Secar plantas silvestres", "Moer em especiaria"),
    "PTBR": (["Dentes-de-leão (Secos)", "Gengibre (Seco)", "Folhas de Uva (Secas)", "Violetas (Secas)",
              "Cardos (Secos)", "Urtigas (Secas)", "Capim-limão (Seco)", "Ginseng (Seco)"],
             "Secar Plantas Silvestres", "Moer como Tempero"),
    "RU": (["Одуванчики (сушёное)", "Корень имбиря (сушёное)", "Виноградные листья (сушёное)", "Фиалки (сушёное)",
            "Чертополох (сушёное)", "Крапива (сушёное)", "Лимонная трава (сушёное)", "Женьшень (сушёное)"],
           "Сушить дикие растения", "Перемолоть в приправу"),
    "CN": (["蒲公英 (干燥)", "生姜 (干燥)", "葡萄叶 (干燥)", "紫罗兰 (干燥)", "洋蓟 (干燥)", "荨麻 (干燥)", "柠檬草 (干燥)",
            "人参 (干燥)"], "晾干野生植物", "研磨成香料"),
    "JP": (["タンポポ(乾燥)", "生姜の根(乾燥)", "ブドウの葉(乾燥)", "スミレ(乾燥)", "アザミ(乾燥)", "イラクサ(乾燥)",
            "レモングラス(乾燥)", "朝鮮人参(乾燥)"], "野草を乾燥させる", "すり潰してスパイスにする"),
    "KO": (["민들레 [마름]", "생강 뿌리 [마름]", "포도 잎 [마름]", "제비꽃 [마름]", "엉겅퀴 [마름]", "쐐기풀 [마름]",
            "레몬그라스 [마름]", "인삼 [마름]"], "야생 식물 말리기", "향신료로 빻기"),
    "TR": (["Kurutulmuş Karahindiba", "Kurutulmuş Zencefil Kökü", "Kurutulmuş Üzüm Yaprağı", "Kurutulmuş Menekşe",
            "Kurutulmuş Devedikeni", "Kurutulmuş Isırgan Otu", "Kurutulmuş Limon Otu", "Kurutulmuş Ginseng"],
           "Yabani Bitkileri Kurut", "Baharat Olarak Öğüt"),
}


# Slices of large fruits: 3 fresh slices, 3 dried slices, then the slicing recipe.
SLICE_ITEMS = ["PineappleSlice", "MangoSlice", "GrapefruitSlice",
               "PineappleSliceDried", "MangoSliceDried", "GrapefruitSliceDried"]
SLICE_T = {
    "EN": (["Pineapple Slice", "Mango Slice", "Grapefruit Slice",
            "Dried Pineapple Slice", "Dried Mango Slice", "Dried Grapefruit Slice"], "Slice Large Fruit"),
    "FR": (["Tranche d'ananas", "Tranche de mangue", "Tranche de pamplemousse",
            "Tranche d'ananas séchée", "Tranche de mangue séchée", "Tranche de pamplemousse séchée"],
           "Couper un gros fruit en tranches"),
    "DE": (["Scheibe Ananas", "Scheibe Mango", "Scheibe Grapefruit",
            "Getrocknete Ananasscheibe", "Getrocknete Mangoscheibe", "Getrocknete Grapefruitscheibe"],
           "Große Frucht schneiden"),
    "ES": (["Rodaja de piña", "Rodaja de mango", "Rodaja de pomelo",
            "Rodaja de piña seca", "Rodaja de mango seca", "Rodaja de pomelo seca"], "Cortar fruta grande"),
    "PT": (["Fatia de ananás", "Fatia de manga", "Fatia de toranja",
            "Fatia de ananás seca", "Fatia de manga seca", "Fatia de toranja seca"], "Fatiar fruta grande"),
    "PTBR": (["Fatia de Abacaxi", "Fatia de Manga", "Fatia de Toranja",
              "Fatia de Abacaxi Seca", "Fatia de Manga Seca", "Fatia de Toranja Seca"], "Fatiar Fruta Grande"),
    "RU": (["Ломтик ананаса", "Ломтик манго", "Ломтик грейпфрута",
            "Сушёный ломтик ананаса", "Сушёный ломтик манго", "Сушёный ломтик грейпфрута"],
           "Нарезать крупный фрукт"),
    "CN": (["菠萝片", "芒果片", "西柚片", "菠萝片干", "芒果片干", "西柚片干"], "大水果切片"),
    "JP": (["パイナップルのカット", "マンゴーのカット", "グレープフルーツのカット",
            "乾燥パイナップルのカット", "乾燥マンゴーのカット", "乾燥グレープフルーツのカット"],
           "大きな果物をスライスする"),
    "KO": (["파인애플 조각", "망고 조각", "자몽 조각", "말린 파인애플 조각", "말린 망고 조각", "말린 자몽 조각"],
           "큰 과일 자르기"),
    "TR": (["Ananas Dilimi", "Mango Dilimi", "Greyfurt Dilimi",
            "Kurutulmuş Ananas Dilimi", "Kurutulmuş Mango Dilimi", "Kurutulmuş Greyfurt Dilimi"],
           "Büyük Meyveyi Dilimle"),
}


# Pemmican: the item, then the recipes without and with dried berries.
PEMMICAN_T = {
    "EN": ("Pemmican", "Make Pemmican", "Make Pemmican with Berries"),
    "FR": ("Pemmican", "Préparer du pemmican", "Préparer du pemmican aux baies"),
    "DE": ("Pemmikan", "Pemmikan herstellen", "Pemmikan mit Beeren herstellen"),
    "ES": ("Pemmican", "Preparar pemmican", "Preparar pemmican con bayas"),
    "PT": ("Pemmican", "Preparar pemmican", "Preparar pemmican com bagas"),
    "PTBR": ("Pemmican", "Preparar Pemmican", "Preparar Pemmican com Frutas Silvestres"),
    "RU": ("Пеммикан", "Приготовить пеммикан", "Приготовить пеммикан с ягодами"),
    "CN": ("干肉饼", "制作干肉饼", "制作浆果干肉饼"),
    "JP": ("ペミカン", "ペミカンを作る", "ベリー入りペミカンを作る"),
    "KO": ("페미컨", "페미컨 만들기", "베리 페미컨 만들기"),
    "TR": ("Pemikan", "Pemikan Yap", "Meyveli Pemikan Yap"),
}


def main():
    for lang, (items, recipes) in T.items():
        assert len(items) == len(ITEMS), (lang, len(items))
        assert len(recipes) == len(RECIPES), (lang, len(recipes))
        wild_items, dry_label, grind_label = WILD_T[lang]
        assert len(wild_items) == len(WILD_ITEMS), lang
        slice_items, slice_label = SLICE_T[lang]
        assert len(slice_items) == len(SLICE_ITEMS), lang
        pem_item, pem_recipe, pem_berries = PEMMICAN_T[lang]
        items = items + wild_items + slice_items + [pem_item]
        recipes = recipes + [dry_label] + [grind_label] * len(HERBS) + [slice_label, pem_recipe, pem_berries]
        folder = os.path.join(ROOT, lang)
        os.makedirs(folder, exist_ok=True)
        names = {"FoodDryingExtended." + k: v for k, v in zip(ITEMS + WILD_ITEMS + SLICE_ITEMS + ["Pemmican"], items)}
        with open(os.path.join(folder, "ItemName.json"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(names, ensure_ascii=False, indent=2) + "\n")
        keys = RECIPES + ["DryWildPlants"] + ["Grind" + h + "Seasoning" for h in HERBS] + ["SliceLargeFruit", "MakePemmican",
                                                                                     "MakePemmicanWithBerries"]
        with open(os.path.join(folder, "Recipes.json"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(dict(zip(keys, recipes)), ensure_ascii=False, indent=2) + "\n")
    print(len(T), "languages written")


main()
