from food import UnitNumber, Food, Nutrition

DAILY_REFER = Nutrition()

DAILY_REFER.nutrition["Energy"] = UnitNumber(2000, "kcal")
DAILY_REFER.nutrition["Protein"] = UnitNumber(50, "g")
DAILY_REFER.nutrition["Fat"] = UnitNumber(78, "g")
DAILY_REFER.nutrition["Carbohydrate"] = UnitNumber(275, "g")
DAILY_REFER.nutrition["Fiber"] = UnitNumber(28, "g")

# DAILY_REFER.nutrition["Calcium, Ca"] = UnitNumber(1300, "mg")
# DAILY_REFER.nutrition["Iron, Fe"] = UnitNumber(18, "mg")
# DAILY_REFER.nutrition["Magnesium, Mg"] = UnitNumber(420, "mg")
# DAILY_REFER.nutrition["Phosphorus, P"] = UnitNumber(1250, "mg")
# DAILY_REFER.nutrition["Potassium, K"] = UnitNumber(4700, "mg")
# DAILY_REFER.nutrition["Sodium, Na"] = UnitNumber(2300, "mg")
# DAILY_REFER.nutrition["Zinc, Zn"] = UnitNumber(11, "mg")
# DAILY_REFER.nutrition["Copper, Cu"] = UnitNumber(0.9, "mg")
# DAILY_REFER.nutrition["Manganese, Mn"] = UnitNumber(2.3, "mg")
# DAILY_REFER.nutrition["Selenium, Se"] = UnitNumber(55, "µg")

DAILY_REFER.nutrition["Vitamin A"] = UnitNumber(900, "µg")
DAILY_REFER.nutrition["Vitamin C"] = UnitNumber(90, "mg")
DAILY_REFER.nutrition["Vitamin E"] = UnitNumber(15, "mg")
# DAILY_REFER.nutrition["Vitamin K"] = UnitNumber(120, "µg")
# DAILY_REFER.nutrition["Vitamin B-6"] = UnitNumber(1.7, "mg")
# DAILY_REFER.nutrition["Vitamin B-12"] = UnitNumber(2.4, "µg")

# DAILY_REFER.nutrition["Thiamin"] = UnitNumber(1.2, "mg")
# DAILY_REFER.nutrition["Riboflavin"] = UnitNumber(1.3, "mg")
# DAILY_REFER.nutrition["Niacin"] = UnitNumber(16, "mg")
# DAILY_REFER.nutrition["Folate, total"] = UnitNumber(400, "µg")
# DAILY_REFER.nutrition["Choline, total"] = UnitNumber(550, "mg")