from dataloader import NutritionDataLoader, PriceDataLoader
from parser import CommandParser
from assistant import Assistant
from history import History, UserInfo
from recommend import Recommender
def handle_help():
    print("""
        help               --  check all available commands
        exit               --  exit the program, will auto save today
        today              --  check nutritions that have been taken today
        eat id n           --  id is fdc_id of food, can be found by search, n is weight in gram 
        search x           --  search food type similar to x 
        recommend m        --  m is mode of recommandation, can choose random, prefer, cheap
        history            --  check history 
        newday             --  start a new day 
        load (path)        --  manually load past history from path, path is optional
        save (path)        --  manually save today to the history, path is optional
        clear (path)       --  clear past history, path is optional
        """)

def handle_eat(assistant, nutrition_loader, args):
    food_id, weight = int(args[0]), float(args[1])
    
    food_type = nutrition_loader.search_by_id(food_id)
    assistant.record(food_type, weight) 
    print("Assistant> Food recorded\n") 

def handle_today(assistant):
    print("Assistant> ", end="")
    assistant.report_today() 

def handle_search(nutrition_loader, args):
    query = args[0] 
    print(f"Assistant> Possible candidates for {query}: \n")
    res = nutrition_loader.search(query) 
    for name, id in res:
        print(f"{name}; fdc_id: {id}")
    print()

def handle_history(history):
    history.check()

def handle_recommend(recommender, args):
    mode = args[0] 
    meal, price = recommender.recommend(mode) 
    print("Assistant> Based on your option, the recommended meal is:")
    print(meal) 
    print(f"Total price {price:.2f}$")
    print()

def handle_newday(assistant, history):
    s = assistant.to_save() 
    history.save(s, new_day=True) 
    assistant.reset() 

def handle_save(assistant, history, args):
    s = assistant.to_save()
    if len(args) > 0:
        history.save(s, path=args[0]) 
    else:
        history.save(s) 

def handle_load(history, args):
    if len(args) > 0:
        history.load(path=args[0]) 
    else:
        history.load() 

def handle_clear(assistant, history, args):
    if len(args) > 0:
        history.clear(path=args[0]) 
    else:
        history.clear() 
    assistant.reset() 
    print("Assistant> past history and today's record cleared")

def autosave(assistant, history, user):
    if assistant.has_eaten():
        s = assistant.to_save()
        history.save(s)
    if user.need_save:
        user.save()

def autoload(assistant, history, nutrition_loader):
    today_meal = history.get_today()
    if today_meal is not None: 
        for food in today_meal["meal"]["foods"]:
            weight = float(food["weight"])
            food_type = nutrition_loader.search_by_name(food["name"])
            assistant.record(food_type, weight) 

def main():
    nutrition_loader = NutritionDataLoader(
        "../data/FoodData_Central_foundation_food_json_2026-04-30.json"
    )
    price_loader = PriceDataLoader(
        "../data/foundation_food_prices_estimated.json"
    )
    user = UserInfo(
        "../preference/user.json"
    )
    parser = CommandParser()
    assistant = Assistant() 
    user.load()
    user_name = user.user_info["user_name"]
    history = History("../history/history.json")
    print("Loading nutrition data...")
    nutrition_loader.load()
    print("Loading price data...")
    price_loader.load()
    print("Loading past history...")
    history.load()
    autoload(assistant, history, nutrition_loader)
    recommender = Recommender(history, assistant, nutrition_loader, price_loader)


    print("----------Nutrition Assistant----------")
    print("Type 'help' to see available commands.")

    while True:
        try:
            user_input = input(f"{user_name}> ").strip()

            if not user_input:
                continue

            command, args = parser.parse(user_input) 

            if not parser.check(command, args):
                print(f"Invalid command: {user_input}")
                continue

            if command == "exit":
                print("Assistant> Goodbye!")
                autosave(assistant, history, user)
                break

            elif command == "help":
                handle_help()

            elif command == "today":
                handle_today(assistant)

            elif command == "search":
                handle_search(nutrition_loader, args)

            elif command == "eat":
                handle_eat(assistant, nutrition_loader, args)

            elif command == "history":
                handle_history(history) 

            elif command == "recommend":
                handle_recommend(recommender, args) 

            elif command == "newday":
                handle_newday(assistant, history) 

            elif command == "load":
                handle_load(history, args)

            elif command == "save":
                handle_save(assistant, history, args) 

            elif command == "clear":
                handle_clear(assistant, history, args) 

            else:
                print(f"Unknown command: {command}")

        except KeyboardInterrupt:
            autosave(assistant, history, user)
            print("Assistant> Goodbye!")
            break

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()