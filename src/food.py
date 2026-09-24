necessity = {
    "Protein": "g", 
    "Energy": "kcal", 
    "Fat": "g", 
    "Fiber": "g", 
    "Carbohydrate": "g", 
    "Vitamin A": "µg",
    "Vitamin C": "mg",
    "Vitamin E": "mg",
    # "Vitamin B-6": "mg",
    # "Vitamin B-12": "µg",
    # "Vitamin K": "µg"
}

mass_mapping = {
    'kg': 1e3, 
    'g': 1, 
    'mg': 1e-3, 
    'µg': 1e-6, 
}

energy_mapping = {
    'kJ': 1e3, 
    'kcal': 4184, 
    'cal': 4.184
}

eps = 1e-8

def transit(value, source_unit, target_unit):
    if source_unit in mass_mapping:
        return value * mass_mapping[source_unit] / mass_mapping[target_unit] 
    elif source_unit in energy_mapping:
        return value * energy_mapping[source_unit] / energy_mapping[target_unit]
    else:
        raise ValueError(f"{source_unit} not supported") 

class UnitNumber: 
    def __init__(self, number, unit):
        self.unit = unit 
        self.number = number 

    def __add__(self, other):
        if self.unit != other.unit:
            other_number = transit(other.number, other.unit, self.unit) 
        else:
            other_number = other.number
        return UnitNumber(self.number + other_number, self.unit)

    def __sub__(self, other):
        if self.unit != other.unit:
            other_number = transit(other.number, other.unit, self.unit)
        else:
            other_number = other.number
        return UnitNumber(max(self.number - other_number, 0), self.unit, )
    
    def __mul__(self, other):
        return UnitNumber(self.number * other, self.unit) 

    def __str__(self):
        return f"{self.number:.2f} {self.unit}" 

    def __eq__(self, other):
        if self.unit != other.unit:
            other_number = transit(other.number, other.unit, self.unit)
        else:
            other_number = other.number
        return abs(self.number - other_number) < eps 

class Nutrition:
    # tuple of different kinds of nutrition 
    def __init__(self, nuts=None):
        self.nutrition = {}
        if nuts is not None:
            for key, unit in necessity.items():
                if key in nuts:
                    res = nuts[key]
                    self.nutrition[key] = UnitNumber(res['amount'], res['unit'])
                else:
                    self.nutrition[key] = UnitNumber(0, unit) 
        else:
            for key, unit in necessity.items():
                self.nutrition[key] = UnitNumber(0, unit)

    def __add__(self, other):
        result = Nutrition() 
        for each in necessity:
            result.nutrition[each] = self.nutrition[each] + other.nutrition[each] 
        return result 

    def __sub__(self, other):
        result = Nutrition() 
        for each in necessity:
            result.nutrition[each] = self.nutrition[each] - other.nutrition[each]
        return result 

    def __mul__(self, other):
        result = Nutrition() 
        for each in necessity:
            result.nutrition[each] = self.nutrition[each] * other
        return result 

    def __str__(self):
        res = "Nutrition List: "
        for key, value in self.nutrition.items():
            res += f"{key}: {value}, "
        res += "\n"
        return res 

    def __eq__(self, other):
        for key in necessity.keys():
            if self.nutrition[key] != other.nutrition[key]:
                return False 
        return True 

class Food:
    def __init__(self, name, weight=None, nuts=None):
        self.name = name 
        self.weight = weight 
        self.nutri_per_gram = Nutrition(nuts) 
        if nuts is not None and weight is not None: 
            self.total_nutri = self.nutri_per_gram * (self.weight / 100)
        else:
            self.total_nutri = None 

    def set_weight(self, weight):
        self.weight = weight 
        self.total_nutri = self.nutri_per_gram * (self.weight / 100)

    def __str__(self):
        res = f"Name: {self.name}, Weight: {self.weight:.2f} g\n"
        res += "Nutrition per 100g: \n"
        res += str(self.nutri_per_gram)
        if self.total_nutri is not None: 
            res += "Total nutrition: \n"
            res += str(self.total_nutri) 
        return res 
    def to_save(self):
        return {
            "name": self.name,
            "weight": self.weight
        }

class Meal: 
    def __init__(self, food_list=None):
        if food_list is None:
            food_list = [] 
        self.food_list = food_list
        self.total_nutri = Nutrition() 
        for each in self.food_list:
            self.total_nutri += each.total_nutri

    def add_food(self, food):
        self.food_list.append(food) 
        self.total_nutri += food.total_nutri

    def __str__(self):
        res = ""
        for each in self.food_list:
            res += f"Name: {each.name}, Weight: {each.weight:.2f} g\n"
        res += str(self.total_nutri)
        return res 

    def to_save(self):
        return {
            "foods": [
                food.to_save()
                for food in self.food_list
            ],
            "total_nutrition": {
                name: {
                    "number": value.number,
                    "unit": value.unit
                }
                for name, value in self.total_nutri.nutrition.items()
            }
        }

if __name__ == "__main__":
    n1 = Nutrition() 
    n2 = Nutrition()
    print(n1 == n2) 
    n1.nutrition["Protein"] += UnitNumber(2, 'g') 
    print(n1 == n2) 