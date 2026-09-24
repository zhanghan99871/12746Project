import json

abbr_mapping = {
    "Total lipid (fat)": "Fat", 
    "Carbohydrate, by difference": "Carbohydrate", 
    "Fiber, total dietary": "Fiber", 
    "Vitamin A, RAE": "Vitamin A", 
    "Vitamin C, total ascorbic acid": "Vitamin C", 
    "Vitamin E (alpha-tocopherol)": "Vitamin E", 
    "Vitamin K (phylloquinone)": "Vitamin K", 

}

class NutritionDataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.food_by_name = {}
        self.food_by_id = {}

    def load(self):
        """Load and process the USDA Foundation Food JSON file."""

        with open(self.file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        raw_foods = raw_data.get("FoundationFoods", [])

        for raw_food in raw_foods:
            if raw_food is None:
                continue
            food = self.process_food(raw_food)
            self.food_by_id[food["fdc_id"]] = food 
            self.food_by_name[food["name"].lower()] = food 

    def process_food(self, raw_food):
        return {
            "fdc_id": raw_food.get("fdcId"),
            "name": raw_food.get("description", ""),
            "nutrients": self.process_nutrients(raw_food),
            "portions": self.process_portions(raw_food),
        }

    def process_nutrients(self, raw_food):
        result = {}

        for item in raw_food.get("foodNutrients", []):
            nutrient = item.get("nutrient", {})

            name = nutrient.get("name")
            unit = nutrient.get("unitName")
            amount = item.get("amount")

            if name is None or amount is None:
                continue

            if name in abbr_mapping:
                name = abbr_mapping[name]

            result[name] = {
                "amount": amount,
                "unit": unit,
                "id": nutrient.get("id"),
            }

        return result

    def process_portions(self, raw_food):
        portions = []

        for portion in raw_food.get("foodPortions", []):
            unit = portion.get("measureUnit", {})

            portions.append({
                "amount": portion.get("amount"),
                "unit": unit.get("name"),
                "abbreviation": unit.get("abbreviation"),
                "gram_weight": portion.get("gramWeight"),
            })

        return portions

    def search_by_name(self, query):
        query = query.lower()
        if query in self.food_by_name:
            return self.food_by_name[query] 
        else:
            raise ValueError(f"Food name {query} not found") 

    def search(self, query):
        query = query.lower()
        result = []

        for food in self.food_by_id.values():
            if query in food["name"].lower():
                result.append(
                    (food["name"], food["fdc_id"])
                )

        return result

    def search_by_id(self, fdc_id):
        if fdc_id not in self.food_by_id:
            raise ValueError(f"Food ID {fdc_id} not found")

        return self.food_by_id[fdc_id]

if __name__ == "__main__":
    loader = NutritionDataLoader(
    "../data/FoodData_Central_foundation_food_json_2026-04-30.json"
    )

    loader.load()
    res = loader.search("egg")
    for each in res:
        print(each)
    test1 = loader.search_by_id(323604)
    print(test1["name"]) 