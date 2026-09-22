necessity = set()
class Nutrition:
    # tuple of different kinds of nutrition 
    def __init__(self, nuts=None):
        self.nutrition = {}
        if nuts is not None:
            for each in necessity:
                self.nutrition[each] = nuts.get(each, 0) 
        else:
            for each in necessity:
                self.nutrition[each] = 0 

    def __add__(self, other):
        result = Nutrition() 
        for each in necessity:
            result.nutrition[each] = self.nutrition[each] + other.nutrition[each] 
        return result 

    def __sub__(self, other):
        result = Nutrition() 
        for each in necessity:
            result.nutrition[each] = max(self.nutrition[each] - other.nutrition[each], 0)
        return result 

    def __mul__(self, other):
        result = Nutrition() 
        for each in necessity:
            result.nutrition[each] = self.nutrition[each] * other
        return result 

class Food:
    def __init__(self, name, weight, nuts):
        self.name = name 
        self.weight = weight 
        self.nutri_per_gram = Nutrition(nuts) 
        self.total_nutri = self.nutri_per_gram * (self.weight / 100)

class Meal: 
    def __init__(self, food_list):
        self.food_list = food_list
        self.total_nutri = Nutrition() 
        for each in self.food_list:
            self.total_nutri += each.total_nutri
