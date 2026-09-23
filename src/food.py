necessity = {
    "Protein": "g", 
    "Energy": "kcal", 
    "Fat": "g", 
    "Fiber": "g", 
    "Carbohydrate": "g", 
    "Vitamin A": "µg",
    "Vitamin C": "mg",
    "Vitamin B-6": "mg",
    "Vitamin B-12": "µg",
    "Vitamin E": "mg",
    "Vitamin K": "µg"
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

class UnitNumber: 
    def __init__(self, number, unit):
        self.unit = unit 
        self.number = number 

    def __add__(self, other):
        if self.unit != other.unit:
            if self.unit in mass_mapping:
                other_number = other.number * mass_mapping[other.unit] / mass_mapping[self.unit]
            else:
                other_number = other.number * energy_mapping[other.unit] / energy_mapping[self.unit]
        else:
            other_number = other.number
        return UnitNumber(self.number + other_number, self.unit)

    def __sub__(self, other):
        if self.unit != other.unit:
            if self.unit in mass_mapping:
                other_number = other.number * mass_mapping[other.unit] / mass_mapping[self.unit]
            else:
                other_number = other.number * energy_mapping[other.unit] / energy_mapping[self.unit]
        else:
            other_number = other.number
        return UnitNumber(max(self.number - other_number, 0), self.unit, )
    
    def __mul__(self, other):
        return UnitNumber(self.number * other, self.unit) 

    def __str__(self):
        return f"{self.number:.2f} {self.unit}" 

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
        res = f"Name: {self.name}, Weight: {self.weight}\n"
        res += "Nutrition per 100g: \n"
        res += str(self.nutri_per_gram)
        if self.total_nutri is not None: 
            res += "Total nutrition: \n"
            res += str(self.total_nutri) 
        return res 

class Meal: 
    def __init__(self, food_list):
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
            res += f"Name: {each.name}, Weight: {each.weight}\n"
        res += str(self.total_nutri)
        return res 
