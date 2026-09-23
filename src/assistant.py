from food import UnitNumber, Food, Nutrition, Meal
from constants import DAILY_REFER
class Assistant: 
    def __init__(self, daily_refer=None):
        self.meal_today = Meal([])
        if daily_refer is not None:
            self.daily_refer = daily_refer 
        else:
            self.daily_refer = DAILY_REFER

    def record(self, food_type, weight):
        food = Food(food_type["name"], weight, food_type["nutrients"])
        self.meal_today.add_food(food) 

    def report_today(self):
        print("Today you have eaten: \n")
        print(self.meal_today) 
        print("You still need following nutrition: \n")
        print(self.daily_refer - self.meal_today.total_nutri) 

if __name__ == "__main__":
    from dataloader import DataLoader
    loader = DataLoader(
        "../data/FoodData_Central_foundation_food_json_2026-04-30.json"
    )
    loader.load()
    assistant = Assistant() 
    food_type = loader.search_by_id(321360)
    print(food_type)
    assistant.record(food_type, 50)
    assistant.report_today()