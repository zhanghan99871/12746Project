from assistant import Assistant
from history import History 
from food import UnitNumber, Nutrition, Food, Meal, necessity, transit
from dataloader import NutritionDataLoader, PriceDataLoader
import random 
from scipy.optimize import linprog
import numpy as np 

def is_useful(condidate:Nutrition, diff:Nutrition):
    if diff - condidate != diff:
        return True 
    else:
        return False 

class Recommender:
    def __init__(self, history:History=None, assistant:Assistant=None, 
                 nutri_loader:NutritionDataLoader=None, price_loader:PriceDataLoader=None,
                 max_amount_per_food=250):
        self.history = history 
        self.assistant = assistant 
        self.nutri_loader = nutri_loader
        self.price_loader = price_loader
        self.max_amount_per_food = max_amount_per_food
        self.price_matrix = None 
        self.nutrition_matrix = None 
        self.id_list = None 

    def update(self, history=None, assistant=None, nutri_loader=None, price_loader=None, max_amount_per_food=None):
        if history is not None:
            self.history = history 
        if assistant is not None:
            self.assistant = assistant
        if nutri_loader is not None:
            self.nutri_loader = nutri_loader
        if price_loader is not None:
            self.price_loader = price_loader 
        if max_amount_per_food is not None: 
            self.max_amount_per_food = max_amount_per_food

    def build_matrix(self):
        self.id_list = list(self.nutri_loader.food_by_id.keys())
        rows = []
        for nutrient, target_unit in necessity.items():
            row = []

            for food_id in self.id_list:
                nutrients = self.nutri_loader.food_by_id[food_id]["nutrients"]

                if nutrient not in nutrients:
                    row.append(0)
                    continue

                data = nutrients[nutrient]

                amount = transit(
                    data["amount"],
                    data["unit"],
                    target_unit
                )

                row.append(amount)

            rows.append(row)

        self.nutrition_matrix = np.array(
            rows,
            dtype=float
        )

        self.price_matrix = np.array([
            self.price_loader.price_by_id[id]["price_usd_per_100g"]
            for id in self.id_list
        ], dtype=float)

    def price_for_meal(self, meal:Meal):
        total_price = 0
        for each in meal.food_list:
            price_per_100g = self.price_loader.search_by_name(each.name)["price_usd_per_100g"]
            total_price += price_per_100g / 100 * each.weight 
        return total_price

    def random_rec(self):
        # randomly pick a meal that satisfy the remaining needs
        diff = self.assistant.diff() 
        zero = Nutrition()
        recommend_meal = Meal() 
        used_set = set()
        while diff != zero:
            random_id = random.choice(list(self.nutri_loader.food_by_id.keys()))
            if random_id in used_set:
                continue
            else:
                used_set.add(random_id) 
            candidate = self.nutri_loader.search_by_id(random_id) 
            food_candidate = Food(candidate["name"], self.max_amount_per_food, candidate["nutrients"])
            if is_useful(food_candidate.total_nutri, diff):
                diff -= food_candidate.total_nutri 
                recommend_meal.add_food(food_candidate) 
        return recommend_meal, self.price_for_meal(recommend_meal)

    def prefer_rec(self):
        # first pick the food appeared in the history, then random pick 
        used_set = set() 
        diff = self.assistant.diff()
        zero = Nutrition() 
        recommend_meal = Meal() 
        for date, meal in self.history.total_hist.items():
            for food in meal["meal"]["foods"]:
                food_name = food["name"]
                candidate = self.nutri_loader.search_by_name(food_name) 
                food_id = candidate["fdc_id"]
                if food_id in used_set:
                    continue 
                else:
                    used_set.add(food_id) 
                food_candidate = Food(candidate["name"], self.max_amount_per_food, candidate["nutrients"])
                if is_useful(food_candidate.total_nutri, diff):
                    diff -= food_candidate.total_nutri 
                    recommend_meal.add_food(food_candidate) 
                if diff == zero:
                    return recommend_meal, self.price_for_meal(recommend_meal)
                
        while diff != zero:
            random_id = random.choice(list(self.nutri_loader.food_by_id.keys()))
            if random_id in used_set:
                continue
            else:
                used_set.add(random_id) 
            candidate = self.nutri_loader.search_by_id(random_id) 
            food_candidate = Food(candidate["name"], self.max_amount_per_food, candidate["nutrients"])
            if is_useful(food_candidate.total_nutri, diff):
                diff -= food_candidate.total_nutri 
                recommend_meal.add_food(food_candidate) 
        return recommend_meal, self.price_for_meal(recommend_meal)

    def cheap_rec(self):
        if self.price_matrix is None or self.nutrition_matrix is None or self.id_list is None: 
            self.build_matrix() 
        diff = self.assistant.diff()
        required = np.array([
            diff.nutrition[name].number
            for name in necessity.keys()
        ], dtype=float)
        result = linprog(
            c=self.price_matrix,
            A_ub=-self.nutrition_matrix,
            b_ub=-required,
            bounds=(0, self.max_amount_per_food / 100),
            method="highs"
        )
        if not result.success:
            raise ValueError(
                f"Optimization failed: {result.message}"
            )

        recommend_meal = Meal()

        for i, amount in enumerate(result.x):
            if amount <= 1e-4:
                continue

            weight = amount * 100

            food_data = self.nutri_loader.search_by_id(self.id_list[i])

            food = Food(
                food_data["name"],
                weight,
                food_data["nutrients"]
            )

            recommend_meal.add_food(food)

        return recommend_meal, self.price_for_meal(recommend_meal)

    def recommend(self, mode):
        if mode == "random":
            return self.random_rec() 
        elif mode == "prefer":
            return self.prefer_rec()
        elif mode == "cheap":
            return self.cheap_rec()
        else:
            print("Not valid option")
            return None 

if __name__ == "__main__":
    nutrition_loader = NutritionDataLoader(
        "../data/FoodData_Central_foundation_food_json_2026-04-30.json"
    )
    assistant = Assistant() 
    history = History("../history/history.json")
    nutrition_loader.load()
    history.load()
    price_loader = PriceDataLoader(
        "../data/foundation_food_prices_estimated.json"
    )
    price_loader.load()
    rec = Recommender(history, assistant, nutrition_loader, price_loader)
    result = rec.cheap_rec()
    print(result[0])
    print(result[1])
        