from command import Command

Commands = {}

class Move(Command):

    def __init__(self):

        def callback(character, args, self):
            direction = args[0]
            currentRoom = character.currentRoom
            print(f"Moving {direction}")
            match direction:
                case "up":
                    character.currentRoom = character.currentRoom.up or currentRoom
                    return 1
                case "down":
                    character.currentRoom = character.currentRoom.down or currentRoom
                    return 1
                case "n":
                    character.currentRoom = character.currentRoom.n or currentRoom
                    return 1
                case "ne":
                    character.currentRoom = character.currentRoom.ne or currentRoom
                    return 1
                case "e":
                    character.currentRoom = character.currentRoom.e or currentRoom
                    return 1
                case "se":
                    character.currentRoom = character.currentRoom.se or currentRoom
                    return 1
                case "s":
                    character.currentRoom = character.currentRoom.s or currentRoom
                    return 1
                case "sw":
                    character.currentRoom = character.currentRoom.sw or currentRoom
                    return 1
                case "w":
                    character.currentRoom = character.currentRoom.w or currentRoom
                    return 1
                case "nw":
                    character.currentRoom = character.currentRoom.nw or currentRoom
                case "_":
                    return 1
            return 0

        super().__init__("move", callback, "Move cardinal + or oridinal x. I'll even let you move up and down :)", 1)
        

class Look(Command):

    def __init__(self):
        def callback(character,args,self):
            print(character.currentRoom.longDesc)

        super().__init__("look", callback, "Take a look around you.", 1)


class Help(Command):

    def __init__(self):
        def callback(character, args, self):
            print("---RTFMan---")
            for name in Commands:
                print(f"{name} - {Commands[name]['description']}")
        super().__init__("look", callback, "What do you think it does?",1)
    

Commands = {
    "move" : Move,
    "look" : Look,
    "dispHelp": Help}
