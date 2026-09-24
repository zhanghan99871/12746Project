import shlex

class CommandParser:

    def parse(self, user_input):
        try:
            tokens = shlex.split(user_input)
        except ValueError as e:
            raise ValueError(f"Invalid command: {e}")

        if not tokens:
            return None, []

        command = tokens[0].lower()
        args = tokens[1:]

        return command, args

    def check(self, command, args):
        if (command == "exit" or command == "history" or command == "help" 
            or command == "today" or command == "newday"):
            return len(args) == 0
        
        elif command == "search":
            return len(args) == 1

        elif command == "eat":
            return len(args) == 2

        elif command == "recommend":
            return len(args) == 1

        elif command == "load" or command == "save" or command == "clear":
            return len(args) == 1 or len(args) == 0 

        return False 
