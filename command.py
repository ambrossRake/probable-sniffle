class Command:
    def __init__(self,name, function, description, accessLevel):
        self.name = name
        self.function = function
        self.description = description
        self.accessLevel = accessLevel

    def run(self, character, args):
        print(args)
        return self.function(character, args,[])
