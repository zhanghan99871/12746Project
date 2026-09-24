from food import UnitNumber, Food, Nutrition, Meal
from constants import DAILY_REFER
from copy import deepcopy
class Assistant: 
    def __init__(self, daily_refer=None):
        self.meal_today = Meal()
        self.satisfied = False 
        if daily_refer is not None:
            self.daily_refer = daily_refer 
        else:
            self.daily_refer = DAILY_REFER

    def reset(self):
        self.meal_today = Meal()
        self.satisfied = False 

    def record(self, food_type, weight):
        food = Food(food_type["name"], weight, food_type["nutrients"])
        self.meal_today.add_food(food) 
        zero = Nutrition()
        diff = self.daily_refer - self.meal_today.total_nutri
        if diff == zero:
            self.satisfied = True 
            print("You have satisfied the nutrition requirement for today!") 

    def diff(self):
        return self.daily_refer - self.meal_today.total_nutri

    def report_today(self):
        print("Today you have eaten: \n")
        print(self.meal_today) 
        print("You still need following nutrition: \n")
        print(self.daily_refer - self.meal_today.total_nutri) 

    def to_save(self):
        return {
            "meal": self.meal_today.to_save(), 
            "satisfied": self.satisfied 
        }

    def has_eaten(self):
        zero = Nutrition()
        return self.meal_today.total_nutri != zero 

if __name__ == "__main__":
    from dataloader import NutritionDataLoader
    loader = NutritionDataLoader(
        "../data/FoodData_Central_foundation_food_json_2026-04-30.json"
    )
    loader.load()
    assistant = Assistant() 
    food_type = loader.search_by_id(321360)
    print(food_type)
    assistant.record(food_type, 50)
    assistant.report_today()