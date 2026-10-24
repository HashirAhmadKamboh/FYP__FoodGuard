import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import AsyncSessionLocal
from app.modules.commodities.models import Commodity, NutritionalProfile

# NOTE:
# Nutrition values are approximate per 100g edible portion unless a serving size is shown separately.
# Actual values can vary by variety, maturity, growing region, and preparation method.

SEED_DATA = [
    # ---------------- FRUIT COMMODITIES ----------------
    {
        "name": 'Apple', "category": 'Fruit',
        "energy_kcal": 49.0, "protein_g": 0.35, "fat_g": 0.1, "carbs_g": 11.8, "fiber_g": 2.0, "water_pct": None,
        "vitamins_minerals": 'Vitamin C (14% RDI), Potassium',
        "phytochemicals": 'Quercetin, Catechins, Chlorogenic Acid, Cyanidin',
        "serving_size": '1 medium (182g)'
    },
    {
        "name": 'Banana', "category": 'Fruit',
        "energy_kcal": 95.0, "protein_g": 1.2, "fat_g": 0.3, "carbs_g": 20.9, "fiber_g": 4.2, "water_pct": None,
        "vitamins_minerals": 'Potassium (450mg), Vit B6',
        "phytochemicals": 'Campesterol, Stigmasterol, Dopamine',
        "serving_size": '1 medium (118g)'
    },
    {
        "name": 'Grape', "category": 'Fruit',
        "energy_kcal": 61.5, "protein_g": 0.4, "fat_g": 0.1, "carbs_g": 15.2, "fiber_g": 0.7, "water_pct": None,
        "vitamins_minerals": 'Vitamin K, Copper',
        "phytochemicals": 'Resveratrol, Myricetin, Anthocyanins, Ellagic Acid',
        "serving_size": '1 cup (151g)'
    },
    {
        "name": 'Guava', "category": 'Fruit',
        "energy_kcal": 68.0, "protein_g": 3.0, "fat_g": 1.0, "carbs_g": 14.0, "fiber_g": 5.0, "water_pct": None,
        "vitamins_minerals": 'Vitamin C (200%+ RDI), Folate',
        "phytochemicals": 'Lycopene, Ellagic Acid, β-carotene',
        "serving_size": '1 medium (55g)'
    },
    {
        "name": 'Jujube', "category": 'Fruit',
        "energy_kcal": 79.0, "protein_g": 1.2, "fat_g": 0.2, "carbs_g": 20.2, "fiber_g": 10.0, "water_pct": '77.9%',
        "vitamins_minerals": 'Vitamin C (69mg), Potassium (250mg)',
        "phytochemicals": 'Flavonoids, Polysaccharides, Triterpenic acids',
        "serving_size": '100g'
    },
    {
        "name": 'Mango', "category": 'Fruit',
        "energy_kcal": 57.0, "protein_g": 0.7, "fat_g": 0.2, "carbs_g": 14.1, "fiber_g": 2.6, "water_pct": None,
        "vitamins_minerals": 'Vitamin A, Vitamin C, Folate',
        "phytochemicals": 'Mangiferin, β-Cryptoxanthin, Gallic Acid',
        "serving_size": '1 cup sliced (165g)'
    },
    {
        "name": 'Orange', "category": 'Fruit',
        "energy_kcal": 37.4, "protein_g": 1.1, "fat_g": 0.1, "carbs_g": 8.5, "fiber_g": 1.7, "water_pct": None,
        "vitamins_minerals": 'Vitamin C, Thiamin (B1)',
        "phytochemicals": 'Hesperidin, Naringenin, Lutein, Tangeritin',
        "serving_size": '1 medium (131g)'
    },
    {
        "name": 'Pomegranate', "category": 'Fruit',
        "energy_kcal": 83.0, "protein_g": 1.7, "fat_g": 1.2, "carbs_g": 18.7, "fiber_g": 4.0, "water_pct": None,
        "vitamins_minerals": 'Vitamin K, Folate, Potassium',
        "phytochemicals": 'Punicalagins, Anthocyanins, Pelargonidin',
        "serving_size": '1/2 cup arils (87g)'
    },
    {
        "name": 'Strawberry', "category": 'Fruit',
        "energy_kcal": 32.0, "protein_g": 0.7, "fat_g": 0.3, "carbs_g": 7.7, "fiber_g": 2.0, "water_pct": None,
        "vitamins_minerals": 'Vitamin C, Manganese',
        "phytochemicals": 'Pelargonidin, Ellagic Acid, Fisetin, Kaempferol',
        "serving_size": '1 cup halves (152g)'
    },
    {
        "name": 'Kinnow', "category": 'Fruit',
        "energy_kcal": 47.0, "protein_g": 0.9, "fat_g": 0.1, "carbs_g": 11.0, "fiber_g": 2.4, "water_pct": '86%',
        "vitamins_minerals": 'Vitamin C, Calcium',
        "phytochemicals": 'Hesperidin, Naringenin, Limonene',
        "serving_size": '1 medium (150g)'
    },
    {
        "name": 'Loquat', "category": 'Fruit',
        "energy_kcal": 47.0, "protein_g": 0.4, "fat_g": 0.2, "carbs_g": 12.1, "fiber_g": 1.7, "water_pct": '86%',
        "vitamins_minerals": 'Vitamin A, Potassium, Manganese',
        "phytochemicals": 'Chlorogenic Acid, Epicatechin, Neochlorogenic Acid',
        "serving_size": '1 cup (149g)'
    },
    {
        "name": 'Lychee', "category": 'Fruit',
        "energy_kcal": 66.0, "protein_g": 0.8, "fat_g": 0.4, "carbs_g": 16.5, "fiber_g": 1.3, "water_pct": '82%',
        "vitamins_minerals": 'Vitamin C, Copper, Potassium',
        "phytochemicals": 'Epicatechin, Rutin',
        "serving_size": '1 cup (190g)'
    },
    {
        "name": 'Melon', "category": 'Fruit',
        "energy_kcal": 34.0, "protein_g": 0.8, "fat_g": 0.2, "carbs_g": 8.2, "fiber_g": 0.9, "water_pct": '90%',
        "vitamins_minerals": 'Vitamin A, Vitamin C, Potassium',
        "phytochemicals": 'Beta-carotene, Lutein, Zeaxanthin',
        "serving_size": '1 cup diced (160g)'
    },
    {
        "name": 'Watermelon', "category": 'Fruit',
        "energy_kcal": 30.0, "protein_g": 0.6, "fat_g": 0.2, "carbs_g": 7.6, "fiber_g": 0.4, "water_pct": '91%',
        "vitamins_minerals": 'Vitamin C, Vitamin A',
        "phytochemicals": 'Lycopene, Citrulline',
        "serving_size": '1 cup diced (152g)'
    },
    {
        "name": 'Peach', "category": 'Fruit',
        "energy_kcal": 39.0, "protein_g": 0.9, "fat_g": 0.3, "carbs_g": 9.5, "fiber_g": 1.5, "water_pct": '89%',
        "vitamins_minerals": 'Vitamin C, Vitamin A, Potassium',
        "phytochemicals": 'Chlorogenic acid, Catechins, Cyanidin',
        "serving_size": '1 medium (150g)'
    },
    {
        "name": 'Plum', "category": 'Fruit',
        "energy_kcal": 46.0, "protein_g": 0.7, "fat_g": 0.3, "carbs_g": 11.4, "fiber_g": 1.4, "water_pct": '87%',
        "vitamins_minerals": 'Vitamin C, Vitamin K',
        "phytochemicals": 'Neochlorogenic acid, Chlorogenic acid',
        "serving_size": '1 medium (66g)'
    },
    {
        "name": 'Apricot', "category": 'Fruit',
        "energy_kcal": 48.0, "protein_g": 1.4, "fat_g": 0.4, "carbs_g": 11.1, "fiber_g": 2.0, "water_pct": '86%',
        "vitamins_minerals": 'Vitamin A, Vitamin C',
        "phytochemicals": 'Beta-carotene, Lutein, Zeaxanthin',
        "serving_size": '2 fresh (70g)'
    },
    {
        "name": 'Falsa', "category": 'Fruit',
        "energy_kcal": 90.0, "protein_g": 1.3, "fat_g": 0.9, "carbs_g": 21.0, "fiber_g": 2.0, "water_pct": '75%',
        "vitamins_minerals": 'Vitamin C, Calcium, Iron',
        "phytochemicals": 'Anthocyanins, Tannins',
        "serving_size": '100g'
    },
    {
        "name": 'Jamun', "category": 'Fruit',
        "energy_kcal": 60.0, "protein_g": 0.7, "fat_g": 0.3, "carbs_g": 14.0, "fiber_g": 0.6, "water_pct": '83%',
        "vitamins_minerals": 'Vitamin C, Iron, Potassium',
        "phytochemicals": 'Anthocyanins, Ellagic acid',
        "serving_size": '100g'
    },
    {
        "name": 'Persimmon', "category": 'Fruit',
        "energy_kcal": 81.0, "protein_g": 0.6, "fat_g": 0.2, "carbs_g": 18.6, "fiber_g": 3.6, "water_pct": '80%',
        "vitamins_minerals": 'Vitamin A, Vitamin C, Manganese',
        "phytochemicals": 'Tannins, Flavonoids, Beta-carotene',
        "serving_size": '1 fruit (168g)'
    },
    {
        "name": 'Pear', "category": 'Fruit',
        "energy_kcal": 57.0, "protein_g": 0.4, "fat_g": 0.1, "carbs_g": 15.2, "fiber_g": 3.1, "water_pct": '84%',
        "vitamins_minerals": 'Vitamin C, Potassium, Copper',
        "phytochemicals": 'Chlorogenic acid, Arbutin, Flavonols',
        "serving_size": '1 medium (178g)'
    },
    {
        "name": 'Papaya', "category": 'Fruit',
        "energy_kcal": 43.0, "protein_g": 0.5, "fat_g": 0.3, "carbs_g": 10.8, "fiber_g": 1.7, "water_pct": '88%',
        "vitamins_minerals": 'Vitamin C, Vitamin A, Folate',
        "phytochemicals": 'Papain, Lycopene, Beta-carotene',
        "serving_size": '1 cup pieces (145g)'
    },
    {
        "name": 'Pineapple', "category": 'Fruit',
        "energy_kcal": 50.0, "protein_g": 0.5, "fat_g": 0.1, "carbs_g": 13.1, "fiber_g": 1.4, "water_pct": '86%',
        "vitamins_minerals": 'Vitamin C, Manganese',
        "phytochemicals": 'Bromelain, Flavonoids, Phenolic acids',
        "serving_size": '1 cup chunks (165g)'
    },
    {
        "name": 'Grapefruit', "category": 'Fruit',
        "energy_kcal": 42.0, "protein_g": 0.8, "fat_g": 0.1, "carbs_g": 10.7, "fiber_g": 1.6, "water_pct": '88%',
        "vitamins_minerals": 'Vitamin C, Vitamin A, Potassium',
        "phytochemicals": 'Naringin, Lycopene, Limonene',
        "serving_size": '1/2 medium (123g)'
    },
    {
        "name": 'Lemon', "category": 'Fruit',
        "energy_kcal": 29.0, "protein_g": 1.1, "fat_g": 0.3, "carbs_g": 9.3, "fiber_g": 2.8, "water_pct": '89%',
        "vitamins_minerals": 'Vitamin C, Potassium',
        "phytochemicals": 'Hesperidin, Diosmin, Limonene, Citric acid',
        "serving_size": '1 fruit (58g)'
    },
    {
        "name": 'Lime', "category": 'Fruit',
        "energy_kcal": 30.0, "protein_g": 0.7, "fat_g": 0.2, "carbs_g": 10.5, "fiber_g": 2.8, "water_pct": '88%',
        "vitamins_minerals": 'Vitamin C, Calcium, Potassium',
        "phytochemicals": 'Limonene, Hesperidin, Naringenin',
        "serving_size": '1 fruit (67g)'
    },
    {
        "name": 'Sweet Lime', "category": 'Fruit',
        "energy_kcal": 43.0, "protein_g": 0.8, "fat_g": 0.3, "carbs_g": 10.4, "fiber_g": 2.0, "water_pct": '88%',
        "vitamins_minerals": 'Vitamin C, Potassium, Calcium',
        "phytochemicals": 'Hesperidin, Naringin, Limonene',
        "serving_size": '1 medium (150g)'
    },
    {
        "name": 'Date', "category": 'Fruit',
        "energy_kcal": 277.0, "protein_g": 1.8, "fat_g": 0.2, "carbs_g": 75.0, "fiber_g": 6.7, "water_pct": '21%',
        "vitamins_minerals": 'Potassium, Magnesium, Copper, Vitamin B6',
        "phytochemicals": 'Phenolic acids, Carotenoids, Flavonoids',
        "serving_size": '2 dates (48g)'
    },
    {
        "name": 'Fig', "category": 'Fruit',
        "energy_kcal": 74.0, "protein_g": 0.8, "fat_g": 0.3, "carbs_g": 19.2, "fiber_g": 2.9, "water_pct": '79%',
        "vitamins_minerals": 'Potassium, Calcium, Magnesium',
        "phytochemicals": 'Anthocyanins, Chlorogenic acid, Rutin',
        "serving_size": '1 medium (50g)'
    },
    {
        "name": 'Mulberry', "category": 'Fruit',
        "energy_kcal": 43.0, "protein_g": 1.4, "fat_g": 0.4, "carbs_g": 9.8, "fiber_g": 1.7, "water_pct": '88%',
        "vitamins_minerals": 'Vitamin C, Iron, Vitamin K',
        "phytochemicals": 'Anthocyanins, Resveratrol, Rutin',
        "serving_size": '1 cup (140g)'
    },
    {
        "name": 'Cherry', "category": 'Fruit',
        "energy_kcal": 50.0, "protein_g": 1.0, "fat_g": 0.3, "carbs_g": 12.2, "fiber_g": 1.6, "water_pct": '86%',
        "vitamins_minerals": 'Vitamin C, Potassium',
        "phytochemicals": 'Anthocyanins, Quercetin, Melatonin',
        "serving_size": '1 cup without pits (154g)'
    },
    {
        "name": 'Coconut', "category": 'Fruit',
        "energy_kcal": 354.0, "protein_g": 3.3, "fat_g": 33.5, "carbs_g": 15.2, "fiber_g": 9.0, "water_pct": '47%',
        "vitamins_minerals": 'Manganese, Copper, Iron',
        "phytochemicals": 'Phenolic acids, Phytosterols',
        "serving_size": '1 piece (45g)'
    },
    {
        "name": 'Sapodilla', "category": 'Fruit',
        "energy_kcal": 83.0, "protein_g": 0.4, "fat_g": 1.1, "carbs_g": 19.9, "fiber_g": 5.3, "water_pct": '78%',
        "vitamins_minerals": 'Vitamin C, Copper, Iron',
        "phytochemicals": 'Tannins, Polyphenols, Carotenoids',
        "serving_size": '1 medium (170g)'
    },
    {
        "name": 'Custard Apple', "category": 'Fruit',
        "energy_kcal": 94.0, "protein_g": 2.1, "fat_g": 0.3, "carbs_g": 23.6, "fiber_g": 4.4, "water_pct": '72%',
        "vitamins_minerals": 'Vitamin C, Vitamin B6, Potassium, Magnesium',
        "phytochemicals": 'Acetogenins, Flavonoids, Phenolic compounds',
        "serving_size": '1 fruit (135g edible)'
    },
    {
        "name": 'Tamarind', "category": 'Fruit',
        "energy_kcal": 239.0, "protein_g": 2.8, "fat_g": 0.6, "carbs_g": 62.5, "fiber_g": 5.1, "water_pct": '31%',
        "vitamins_minerals": 'Thiamin (B1), Magnesium, Potassium, Iron',
        "phytochemicals": 'Tartaric acid, Polyphenols, Flavonoids',
        "serving_size": '1/4 cup pulp (30g)'
    },
    {
        "name": 'Jackfruit', "category": 'Fruit',
        "energy_kcal": 95.0, "protein_g": 1.7, "fat_g": 0.6, "carbs_g": 23.3, "fiber_g": 1.5, "water_pct": '73%',
        "vitamins_minerals": 'Vitamin C, Potassium, Vitamin B6',
        "phytochemicals": 'Carotenoids, Lignans, Isoflavones',
        "serving_size": '1 cup sliced (165g)'
    },
    {
        "name": 'Amla', "category": 'Fruit',
        "energy_kcal": 44.0, "protein_g": 0.9, "fat_g": 0.6, "carbs_g": 10.2, "fiber_g": 4.3, "water_pct": '87%',
        "vitamins_minerals": 'Very high Vitamin C, Calcium, Iron',
        "phytochemicals": 'Emblicanin, Gallic acid, Ellagic acid, Tannins',
        "serving_size": '100g'
    },
    {
        "name": 'Avocado', "category": 'Fruit',
        "energy_kcal": 160.0, "protein_g": 2.0, "fat_g": 14.7, "carbs_g": 8.5, "fiber_g": 6.7, "water_pct": '73%',
        "vitamins_minerals": 'Potassium, Vitamin E, Folate, Vitamin K',
        "phytochemicals": 'Lutein, Zeaxanthin, Phytosterols',
        "serving_size": '1/2 fruit (100g)'
    },

    # ---------------- VEGETABLE COMMODITIES ----------------
    {
        "name": 'Bell Pepper / Shimla Mirch', "category": 'Vegetable',
        "energy_kcal": 20.0, "protein_g": 0.9, "fat_g": 0.2, "carbs_g": 4.6, "fiber_g": 1.7, "water_pct": None,
        "vitamins_minerals": 'Vitamin C (150% RDI), Vit B6',
        "phytochemicals": 'Lutein, Zeaxanthin, Quercetin, Luteolin',
        "serving_size": '1 medium (119g)'
    },
    {
        "name": 'Bitter Gourd / Karela', "category": 'Vegetable',
        "energy_kcal": 17.0, "protein_g": 1.0, "fat_g": 0.2, "carbs_g": 3.7, "fiber_g": 2.8, "water_pct": None,
        "vitamins_minerals": 'Vitamin C, Folate, Magnesium',
        "phytochemicals": 'Charantin, Vicine, Polypeptide-p (Plant Insulin)',
        "serving_size": '1 cup (93g)'
    },
    {
        "name": 'Capsicum / Shimla Mirch', "category": 'Vegetable',
        "energy_kcal": 20.0, "protein_g": 0.9, "fat_g": 0.2, "carbs_g": 4.6, "fiber_g": 1.7, "water_pct": None,
        "vitamins_minerals": 'Vitamin C, Vitamin A',
        "phytochemicals": 'Capsaicinoids (trace), Lutein, Flavones',
        "serving_size": '1 medium (119g)'
    },
    {
        "name": 'Carrot / Gajar', "category": 'Vegetable',
        "energy_kcal": 41.0, "protein_g": 0.9, "fat_g": 0.2, "carbs_g": 10.0, "fiber_g": 2.8, "water_pct": None,
        "vitamins_minerals": 'Vitamin A (β-carotene), Vit K',
        "phytochemicals": 'α-Carotene, β-Carotene, Luteolin',
        "serving_size": '1 medium (61g)'
    },
    {
        "name": 'Cucumber / Kheera', "category": 'Vegetable',
        "energy_kcal": 15.0, "protein_g": 0.6, "fat_g": 0.1, "carbs_g": 3.6, "fiber_g": 0.5, "water_pct": None,
        "vitamins_minerals": 'Vitamin K, Potassium',
        "phytochemicals": 'Cucurbitacins, Fisetin, Beta-sitosterol',
        "serving_size": '1/2 cup sliced (52g)'
    },
    {
        "name": 'Okra / Bhindi', "category": 'Vegetable',
        "energy_kcal": 30.0, "protein_g": 1.7, "fat_g": 0.2, "carbs_g": 6.6, "fiber_g": 2.2, "water_pct": None,
        "vitamins_minerals": 'Folate (37% RDI), Manganese',
        "phytochemicals": 'Quercetin, Catechin, Epicatechin',
        "serving_size": '1/2 cup (80g)'
    },
    {
        "name": 'Potato / Aloo', "category": 'Vegetable',
        "energy_kcal": 67.0, "protein_g": 1.6, "fat_g": 0.1, "carbs_g": 15.0, "fiber_g": 2.0, "water_pct": None,
        "vitamins_minerals": 'Vitamin C, Potassium, Vit B6',
        "phytochemicals": 'Chlorogenic Acid, Caffeic Acid, Patatin',
        "serving_size": '1 medium (173g)'
    },
    {
        "name": 'Tomato / Tamatar', "category": 'Vegetable',
        "energy_kcal": 18.0, "protein_g": 0.9, "fat_g": 0.2, "carbs_g": 3.9, "fiber_g": 1.2, "water_pct": None,
        "vitamins_minerals": 'Vitamin C, Potassium, Folate',
        "phytochemicals": 'Lycopene, Naringenin, Rutin, Chlorogenic Acid',
        "serving_size": '1 medium (123g)'
    },
    {
        "name": 'Onion / Pyaz', "category": 'Vegetable',
        "energy_kcal": 40.0, "protein_g": 1.1, "fat_g": 0.1, "carbs_g": 9.3, "fiber_g": 1.7, "water_pct": '89%',
        "vitamins_minerals": 'Vitamin C, Vitamin B6, Potassium',
        "phytochemicals": 'Quercetin, Sulfur compounds, Anthocyanins',
        "serving_size": '1 medium (110g)'
    },
    {
        "name": 'Garlic / Lehsan', "category": 'Vegetable',
        "energy_kcal": 149.0, "protein_g": 6.4, "fat_g": 0.5, "carbs_g": 33.1, "fiber_g": 2.1, "water_pct": '59%',
        "vitamins_minerals": 'Manganese, Vitamin B6, Vitamin C, Selenium',
        "phytochemicals": 'Allicin, Diallyl sulfides, Saponins',
        "serving_size": '3 cloves (9g)'
    },
    {
        "name": 'Ginger / Adrak', "category": 'Vegetable',
        "energy_kcal": 80.0, "protein_g": 1.8, "fat_g": 0.8, "carbs_g": 17.8, "fiber_g": 2.0, "water_pct": '79%',
        "vitamins_minerals": 'Magnesium, Potassium, Vitamin B6',
        "phytochemicals": 'Gingerol, Shogaol, Zingerone',
        "serving_size": '1 tbsp sliced (6g)'
    },
    {
        "name": 'Green Chili / Hari Mirch', "category": 'Vegetable',
        "energy_kcal": 40.0, "protein_g": 2.0, "fat_g": 0.2, "carbs_g": 9.5, "fiber_g": 1.5, "water_pct": '88%',
        "vitamins_minerals": 'Vitamin C, Vitamin A, Potassium',
        "phytochemicals": 'Capsaicin, Lutein, Zeaxanthin',
        "serving_size": '1 chili (15g)'
    },
    {
        "name": 'Cabbage / Band Gobi', "category": 'Vegetable',
        "energy_kcal": 25.0, "protein_g": 1.3, "fat_g": 0.1, "carbs_g": 5.8, "fiber_g": 2.5, "water_pct": '92%',
        "vitamins_minerals": 'Vitamin C, Vitamin K, Folate',
        "phytochemicals": 'Glucosinolates, Anthocyanins, Sulforaphane',
        "serving_size": '1 cup chopped (89g)'
    },
    {
        "name": 'Cauliflower / Phool Gobi', "category": 'Vegetable',
        "energy_kcal": 25.0, "protein_g": 1.9, "fat_g": 0.3, "carbs_g": 5.0, "fiber_g": 2.0, "water_pct": '92%',
        "vitamins_minerals": 'Vitamin C, Vitamin K, Folate',
        "phytochemicals": 'Glucosinolates, Sulforaphane, Indole-3-carbinol',
        "serving_size": '1 cup chopped (107g)'
    },
    {
        "name": 'Broccoli / Broccoli', "category": 'Vegetable',
        "energy_kcal": 34.0, "protein_g": 2.8, "fat_g": 0.4, "carbs_g": 6.6, "fiber_g": 2.6, "water_pct": '89%',
        "vitamins_minerals": 'Vitamin C, Vitamin K, Folate',
        "phytochemicals": 'Sulforaphane, Glucosinolates, Lutein',
        "serving_size": '1 cup chopped (91g)'
    },
    {
        "name": 'Spinach / Palak', "category": 'Vegetable',
        "energy_kcal": 23.0, "protein_g": 2.9, "fat_g": 0.4, "carbs_g": 3.6, "fiber_g": 2.2, "water_pct": '91%',
        "vitamins_minerals": 'Vitamin K, Vitamin A, Folate, Iron',
        "phytochemicals": 'Lutein, Zeaxanthin, Quercetin',
        "serving_size": '1 cup raw (30g)'
    },
    {
        "name": 'Mustard Greens / Sarson ka Saag', "category": 'Vegetable',
        "energy_kcal": 27.0, "protein_g": 2.9, "fat_g": 0.4, "carbs_g": 4.7, "fiber_g": 3.2, "water_pct": '90%',
        "vitamins_minerals": 'Vitamin K, Vitamin A, Vitamin C, Calcium',
        "phytochemicals": 'Glucosinolates, Isothiocyanates, Flavonoids',
        "serving_size": '1 cup chopped (56g)'
    },
    {
        "name": 'Fenugreek Leaves / Methi', "category": 'Vegetable',
        "energy_kcal": 49.0, "protein_g": 4.4, "fat_g": 0.9, "carbs_g": 6.0, "fiber_g": 1.1, "water_pct": '86%',
        "vitamins_minerals": 'Iron, Calcium, Vitamin C, Folate',
        "phytochemicals": 'Saponins, Flavonoids, Trigonelline',
        "serving_size": '1 cup chopped (100g)'
    },
    {
        "name": 'Coriander Leaves / Dhania', "category": 'Vegetable',
        "energy_kcal": 23.0, "protein_g": 2.1, "fat_g": 0.5, "carbs_g": 3.7, "fiber_g": 2.8, "water_pct": '92%',
        "vitamins_minerals": 'Vitamin K, Vitamin C, Potassium',
        "phytochemicals": 'Linalool, Quercetin, Phenolic acids',
        "serving_size": '1 cup (16g)'
    },
    {
        "name": 'Mint Leaves / Pudina', "category": 'Vegetable',
        "energy_kcal": 44.0, "protein_g": 3.3, "fat_g": 0.7, "carbs_g": 8.4, "fiber_g": 6.8, "water_pct": '85%',
        "vitamins_minerals": 'Vitamin A, Iron, Manganese',
        "phytochemicals": 'Menthol, Rosmarinic acid, Flavonoids',
        "serving_size": '1/4 cup chopped (14g)'
    },
    {
        "name": 'Lettuce / Salad Patta', "category": 'Vegetable',
        "energy_kcal": 15.0, "protein_g": 1.4, "fat_g": 0.2, "carbs_g": 2.9, "fiber_g": 1.3, "water_pct": '95%',
        "vitamins_minerals": 'Vitamin K, Vitamin A, Folate',
        "phytochemicals": 'Lutein, Beta-carotene, Quercetin',
        "serving_size": '1 cup shredded (36g)'
    },
    {
        "name": 'Brinjal / Baingan', "category": 'Vegetable',
        "energy_kcal": 25.0, "protein_g": 1.0, "fat_g": 0.2, "carbs_g": 5.9, "fiber_g": 3.0, "water_pct": '92%',
        "vitamins_minerals": 'Manganese, Folate, Potassium',
        "phytochemicals": 'Nasunin, Chlorogenic acid, Anthocyanins',
        "serving_size": '1 cup cubes (82g)'
    },
    {
        "name": 'Bottle Gourd / Lauki', "category": 'Vegetable',
        "energy_kcal": 14.0, "protein_g": 0.6, "fat_g": 0.02, "carbs_g": 3.4, "fiber_g": 0.5, "water_pct": '96%',
        "vitamins_minerals": 'Vitamin C, Potassium, Calcium',
        "phytochemicals": 'Cucurbitacins, Flavonoids, Phenolic compounds',
        "serving_size": '1 cup chopped (116g)'
    },
    {
        "name": 'Ridge Gourd / Tori', "category": 'Vegetable',
        "energy_kcal": 20.0, "protein_g": 1.2, "fat_g": 0.2, "carbs_g": 4.4, "fiber_g": 1.1, "water_pct": '94%',
        "vitamins_minerals": 'Vitamin C, Zinc, Iron',
        "phytochemicals": 'Flavonoids, Saponins, Cucurbitacins',
        "serving_size": '1 cup chopped (100g)'
    },
    {
        "name": 'Sponge Gourd / Tori', "category": 'Vegetable',
        "energy_kcal": 18.0, "protein_g": 0.7, "fat_g": 0.2, "carbs_g": 3.6, "fiber_g": 1.2, "water_pct": '95%',
        "vitamins_minerals": 'Vitamin C, Potassium, Magnesium',
        "phytochemicals": 'Cucurbitacins, Flavonoids, Triterpenoids',
        "serving_size": '1 cup chopped (100g)'
    },
    {
        "name": 'Pumpkin / Kaddu', "category": 'Vegetable',
        "energy_kcal": 26.0, "protein_g": 1.0, "fat_g": 0.1, "carbs_g": 6.5, "fiber_g": 0.5, "water_pct": '92%',
        "vitamins_minerals": 'Vitamin A, Vitamin C, Potassium',
        "phytochemicals": 'Beta-carotene, Lutein, Zeaxanthin',
        "serving_size": '1 cup cubes (116g)'
    },
    {
        "name": 'Round Gourd / Tinda', "category": 'Vegetable',
        "energy_kcal": 21.0, "protein_g": 1.4, "fat_g": 0.2, "carbs_g": 3.4, "fiber_g": 1.6, "water_pct": '94%',
        "vitamins_minerals": 'Vitamin C, Potassium, Magnesium',
        "phytochemicals": 'Flavonoids, Phenolic compounds, Cucurbitacins',
        "serving_size": '1 cup chopped (100g)'
    },
    {
        "name": 'Pointed Gourd / Parwal', "category": 'Vegetable',
        "energy_kcal": 20.0, "protein_g": 1.4, "fat_g": 0.4, "carbs_g": 4.0, "fiber_g": 2.0, "water_pct": '93%',
        "vitamins_minerals": 'Vitamin A, Vitamin C, Potassium',
        "phytochemicals": 'Flavonoids, Triterpenoids, Cucurbitacins',
        "serving_size": '1 cup chopped (100g)'
    },
    {
        "name": 'Snake Gourd / Chichinda', "category": 'Vegetable',
        "energy_kcal": 18.0, "protein_g": 0.5, "fat_g": 0.3, "carbs_g": 3.3, "fiber_g": 0.8, "water_pct": '95%',
        "vitamins_minerals": 'Vitamin C, Calcium, Magnesium',
        "phytochemicals": 'Cucurbitacins, Flavonoids, Carotenoids',
        "serving_size": '1 cup chopped (100g)'
    },
    {
        "name": 'Ash Gourd / Petha Kaddu', "category": 'Vegetable',
        "energy_kcal": 13.0, "protein_g": 0.4, "fat_g": 0.2, "carbs_g": 3.0, "fiber_g": 2.9, "water_pct": '96%',
        "vitamins_minerals": 'Vitamin C, Calcium, Iron',
        "phytochemicals": 'Flavonoids, Triterpenes, Cucurbitacins',
        "serving_size": '1 cup cubes (100g)'
    },
    {
        "name": 'Peas / Matar', "category": 'Vegetable',
        "energy_kcal": 81.0, "protein_g": 5.4, "fat_g": 0.4, "carbs_g": 14.5, "fiber_g": 5.1, "water_pct": '79%',
        "vitamins_minerals": 'Vitamin K, Vitamin C, Folate, Manganese',
        "phytochemicals": 'Lutein, Zeaxanthin, Saponins',
        "serving_size": '1/2 cup (80g)'
    },
    {
        "name": 'Green Beans / Phalian', "category": 'Vegetable',
        "energy_kcal": 31.0, "protein_g": 1.8, "fat_g": 0.2, "carbs_g": 7.1, "fiber_g": 3.4, "water_pct": '90%',
        "vitamins_minerals": 'Vitamin C, Vitamin K, Folate',
        "phytochemicals": 'Lutein, Beta-carotene, Quercetin',
        "serving_size": '1 cup (100g)'
    },
    {
        "name": 'Cluster Beans / Gawar Phali', "category": 'Vegetable',
        "energy_kcal": 35.0, "protein_g": 3.2, "fat_g": 0.3, "carbs_g": 7.9, "fiber_g": 3.0, "water_pct": '88%',
        "vitamins_minerals": 'Vitamin C, Calcium, Iron',
        "phytochemicals": 'Galactomannan, Flavonoids, Phenolic compounds',
        "serving_size": '1 cup chopped (100g)'
    },
    {
        "name": 'Broad Beans / Bakla', "category": 'Vegetable',
        "energy_kcal": 88.0, "protein_g": 7.9, "fat_g": 0.7, "carbs_g": 17.6, "fiber_g": 5.4, "water_pct": '72%',
        "vitamins_minerals": 'Folate, Manganese, Iron, Magnesium',
        "phytochemicals": 'L-dopa, Flavonoids, Phenolic acids',
        "serving_size": '1/2 cup (85g)'
    },
    {
        "name": 'Radish / Mooli', "category": 'Vegetable',
        "energy_kcal": 16.0, "protein_g": 0.7, "fat_g": 0.1, "carbs_g": 3.4, "fiber_g": 1.6, "water_pct": '95%',
        "vitamins_minerals": 'Vitamin C, Potassium, Folate',
        "phytochemicals": 'Isothiocyanates, Anthocyanins, Indoles',
        "serving_size": '1 cup sliced (116g)'
    },
    {
        "name": 'Turnip / Shalgam', "category": 'Vegetable',
        "energy_kcal": 28.0, "protein_g": 0.9, "fat_g": 0.1, "carbs_g": 6.4, "fiber_g": 1.8, "water_pct": '92%',
        "vitamins_minerals": 'Vitamin C, Potassium, Calcium',
        "phytochemicals": 'Glucosinolates, Isothiocyanates, Phenolic acids',
        "serving_size": '1 medium (122g)'
    },
    {
        "name": 'Beetroot / Chukandar', "category": 'Vegetable',
        "energy_kcal": 43.0, "protein_g": 1.6, "fat_g": 0.2, "carbs_g": 9.6, "fiber_g": 2.8, "water_pct": '88%',
        "vitamins_minerals": 'Folate, Manganese, Potassium',
        "phytochemicals": 'Betalains, Nitrates, Phenolic acids',
        "serving_size": '1/2 cup sliced (85g)'
    },
    {
        "name": 'Sweet Potato / Shakarkandi', "category": 'Vegetable',
        "energy_kcal": 86.0, "protein_g": 1.6, "fat_g": 0.1, "carbs_g": 20.1, "fiber_g": 3.0, "water_pct": '77%',
        "vitamins_minerals": 'Vitamin A, Vitamin C, Potassium',
        "phytochemicals": 'Beta-carotene, Anthocyanins, Chlorogenic acid',
        "serving_size": '1 medium (130g)'
    },
    {
        "name": 'Taro Root / Arvi', "category": 'Vegetable',
        "energy_kcal": 112.0, "protein_g": 1.5, "fat_g": 0.2, "carbs_g": 26.5, "fiber_g": 4.1, "water_pct": '70%',
        "vitamins_minerals": 'Potassium, Manganese, Vitamin E',
        "phytochemicals": 'Polyphenols, Resistant starch, Saponins',
        "serving_size": '1 cup sliced (104g)'
    },
    {
        "name": 'Yam / Zimikand', "category": 'Vegetable',
        "energy_kcal": 118.0, "protein_g": 1.5, "fat_g": 0.2, "carbs_g": 27.9, "fiber_g": 4.1, "water_pct": '70%',
        "vitamins_minerals": 'Potassium, Vitamin C, Manganese',
        "phytochemicals": 'Diosgenin, Saponins, Phenolic compounds',
        "serving_size": '1 cup cubes (136g)'
    },
    {
        "name": 'Lotus Root / Bhein', "category": 'Vegetable',
        "energy_kcal": 74.0, "protein_g": 2.6, "fat_g": 0.1, "carbs_g": 17.2, "fiber_g": 4.9, "water_pct": '80%',
        "vitamins_minerals": 'Vitamin C, Copper, Potassium',
        "phytochemicals": 'Polyphenols, Tannins, Flavonoids',
        "serving_size": '1 cup slices (120g)'
    },
    {
        "name": 'Sweet Corn / Makai', "category": 'Vegetable',
        "energy_kcal": 86.0, "protein_g": 3.2, "fat_g": 1.2, "carbs_g": 19.0, "fiber_g": 2.7, "water_pct": '76%',
        "vitamins_minerals": 'Thiamin (B1), Folate, Magnesium',
        "phytochemicals": 'Lutein, Zeaxanthin, Ferulic acid',
        "serving_size": '1 medium ear (90g)'
    },
    {
        "name": 'Mushroom / Khumbi', "category": 'Vegetable',
        "energy_kcal": 22.0, "protein_g": 3.1, "fat_g": 0.3, "carbs_g": 3.3, "fiber_g": 1.0, "water_pct": '92%',
        "vitamins_minerals": 'Riboflavin (B2), Niacin (B3), Selenium',
        "phytochemicals": 'Ergothioneine, Beta-glucans, Phenolic compounds',
        "serving_size": '1 cup pieces (70g)'
    },
    {
        "name": 'Spring Onion / Hara Pyaz', "category": 'Vegetable',
        "energy_kcal": 32.0, "protein_g": 1.8, "fat_g": 0.2, "carbs_g": 7.3, "fiber_g": 2.6, "water_pct": '89%',
        "vitamins_minerals": 'Vitamin K, Vitamin C, Folate',
        "phytochemicals": 'Quercetin, Sulfur compounds, Flavonoids',
        "serving_size": '1 cup chopped (100g)'
    },
    {
        "name": 'Leek / Gandana', "category": 'Vegetable',
        "energy_kcal": 61.0, "protein_g": 1.5, "fat_g": 0.3, "carbs_g": 14.2, "fiber_g": 1.8, "water_pct": '83%',
        "vitamins_minerals": 'Vitamin K, Manganese, Vitamin C',
        "phytochemicals": 'Kaempferol, Allicin-related sulfur compounds',
        "serving_size": '1 cup chopped (89g)'
    },
    {
        "name": 'Drumstick Pods / Sohanjna', "category": 'Vegetable',
        "energy_kcal": 37.0, "protein_g": 2.1, "fat_g": 0.2, "carbs_g": 8.5, "fiber_g": 3.2, "water_pct": '89%',
        "vitamins_minerals": 'Vitamin C, Potassium, Magnesium',
        "phytochemicals": 'Isothiocyanates, Quercetin, Chlorogenic acid',
        "serving_size": '1 cup chopped (100g)'
    },
    {
        "name": 'Kohlrabi / Ganth Gobi', "category": 'Vegetable',
        "energy_kcal": 27.0, "protein_g": 1.7, "fat_g": 0.1, "carbs_g": 6.2, "fiber_g": 3.6, "water_pct": '91%',
        "vitamins_minerals": 'Vitamin C, Potassium, Vitamin B6',
        "phytochemicals": 'Glucosinolates, Isothiocyanates, Anthocyanins',
        "serving_size": '1 cup slices (135g)'
    },

    # ---------------- ANIMAL-DERIVED PROTEINS ----------------
    {
        "name": 'Meat (Beef)', "category": 'Others',
        "energy_kcal": 250.0, "protein_g": 26.0, "fat_g": 17.0, "carbs_g": 0.0, "fiber_g": 0.0, "water_pct": '60-70%',
        "vitamins_minerals": 'Iron, Zinc, Vitamin B12, Selenium',
        "phytochemicals": 'Creatine, Carnosine, Conjugated Linoleic Acid (CLA)',
        "serving_size": '3 oz (85g)'
    },
    {
        "name": 'Chicken', "category": 'Others',
        "energy_kcal": 165.0, "protein_g": 31.0, "fat_g": 3.6, "carbs_g": 0.0, "fiber_g": 0.0, "water_pct": '65-75%',
        "vitamins_minerals": 'Niacin (B3), Selenium, Phosphorus',
        "phytochemicals": 'Anserine, Taurine, Carnosine',
        "serving_size": '3 oz (85g)'
    },
    {
        "name": 'Fish', "category": 'Others',
        "energy_kcal": 120.0, "protein_g": 22.0, "fat_g": 3.0, "carbs_g": 0.0, "fiber_g": 0.0, "water_pct": '70-80%',
        "vitamins_minerals": 'Vitamin D, Iodine, Selenium',
        "phytochemicals": 'Eicosapentaenoic Acid (EPA), Docosahexaenoic Acid (DHA)',
        "serving_size": '3 oz (85g)'
    },
    {
        "name": 'Egg', "category": 'Others',
        "energy_kcal": 155.0, "protein_g": 13.0, "fat_g": 11.0, "carbs_g": 0.0, "fiber_g": 0.0, "water_pct": '76%',
        "vitamins_minerals": 'Choline, Riboflavin, Vitamin B12',
        "phytochemicals": 'Lutein, Zeaxanthin, Phosvitin',
        "serving_size": '1 large (50g)'
    },
]

async def seed_ingredients():
    async with AsyncSessionLocal() as session:
        try:
            # Ensure tables exist
            async with session.bind.begin() as conn:
                from app.db.base import Base
                await conn.run_sync(Base.metadata.create_all)

            # --- NEW SMART CHECK ---
            # If there is already at least 1 commodity, skip seeding to avoid crashes!
            existing = await session.execute(select(Commodity).limit(1))
            if existing.scalar_one_or_none():
                print("🌱 [SEED] Nutritional data already exists. Skipping seed.")
                return

            print("🌱 [SEED] Database is empty. Seeding Nutritional Data now...")
            for item_data in SEED_DATA:
                # 1. Create the Commodity
                commodity = Commodity(
                    name=item_data["name"], 
                    category=item_data["category"]
                )
                session.add(commodity)
                await session.flush() # Flush to generate the commodity ID

                # 2. Create the associated Nutritional Profile
                nutrition = NutritionalProfile(
                    commodity_id=commodity.id,
                    energy_kcal=item_data["energy_kcal"],
                    protein_g=item_data["protein_g"],
                    fat_g=item_data["fat_g"],
                    carbs_g=item_data["carbs_g"],
                    fiber_g=item_data["fiber_g"],
                    water_pct=item_data["water_pct"],
                    vitamins_minerals=item_data["vitamins_minerals"],
                    phytochemicals=item_data["phytochemicals"],
                    serving_size=item_data.get("serving_size")
                )
                session.add(nutrition)

            # 3. Commit the transaction to the database
            await session.commit()
            print(f"✅ [SEED] Successfully seeded {len(SEED_DATA)} ingredients into the database!")

        except Exception as e:
            await session.rollback()
            print(f"❌ [SEED] Error seeding data: {e}")

if __name__ == "__main__":
    asyncio.run(seed_ingredients())
