from dataloader import DataLoader
from parser import CommandParser
from assistant import Assistant
def handle_help():
    print("""
        help               --  check all available commands
        exit               --  exit the program
        today              --  check nutritions that have been taken today
        eat id n           --  id is fdc_id of food, can be found by search, n is weight in gram 
        search x           --  search food type similar to x 
        recommend m        --  m is mode of recommandation, can choose random, prefer, cheap
        history            --  check history 
        """)

def handle_eat(assistant, loader, args):
    food_id, weight = int(args[0]), float(args[1])
    
    food_type = loader.search_by_id(food_id)
    assistant.record(food_type, weight) 
    print("Food recorded\n") 

def handle_today(assistant):
    assistant.report_today() 

def handle_search(loader, args):
    query = args[0] 
    print(f"Possible candidates for {query}: \n")
    res = loader.search(query) 
    for name, id in res:
        print(f"{name}; fdc_id: {id}")

def handle_history():
    raise NotImplementedError 

def handle_recommend(args):
    raise NotImplementedError 

def main():
    loader = DataLoader(
        "../data/FoodData_Central_foundation_food_json_2026-04-30.json"
    )
    parser = CommandParser()
    assistant = Assistant() 
    loader.load()

    print("Nutrition Assistant")
    print("Type 'help' to see available commands.")

    while True:
        try:
            user_input = input("FoodHelper> ").strip()

            if not user_input:
                continue

            command, args = parser.parse(user_input) 

            if not parser.check(command, args):
                print(f"Invalid command: {user_input}")
                continue

            if command == "exit":
                print("Goodbye!")
                break

            elif command == "help":
                handle_help()

            elif command == "today":
                handle_today(assistant)

            elif command == "search":
                handle_search(loader, args)

            elif command == "eat":
                handle_eat(assistant, loader, args)

            elif command == "history":
                handle_history()

            elif command == "recommend":
                handle_recommend(args) 

            else:
                print(f"Unknown command: {command}")

        except KeyboardInterrupt:
            print("Goodbye!")
            break

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()