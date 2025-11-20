import os
import time
from enum import Enum

gameRunning = True;
commands = {};
currentPrompt = "";
promptUser = True
textAnimSpeed = .005
player = {}

class Character:

    def __init__(self,name = "", age = 0, eddies = 0, reputation = 0, inventory = {}, accessLevel = 0):
        self.name = name
        self.age = age
        self.eddies = eddies
        self.rep = reputation
        self.inventory = inventory
        self.accessLevel = accessLevel


player["Character"] = Character()

class States(Enum):
    MAIN_MENU = 0
    NIGHT_CITY = 1
    RIPPER_DOC = 2
    MEAT_SPACE = 3
    

currentState = States.MAIN_MENU


class Item:
    def __init__(self, name, desc, func):
        self.name = name
        self.desc = desc
        self.func = func

    def use(self,params):
        self.func(params)

def test():
    print('Used cyberdeck')
    
docsCyberdeck = Item("Old Cyberdeck", "An old cyberdeck", test)

class Room:
    def __init__(self, description,longDescription):
        self.desc = description
        self.longDesc = longDescription
        self.n = None
        self.ne = None
        self.e = None
        self.se = None
        self.s = None
        self.sw = None
        self.w = None
        self.nw = None
        self.up = None
        self.down = None
        self.visited = False
        self.items = {}

    def getItemDesc(self):
        plural = ""
        if len(self.items) > 1:
            plural = "are"
        elif len(self.items) == 1:
            plural = "is"
        else:
            return ""
        itemDesc = f"There {plural} "
        for item in self.items:
            itemDesc += "a " + item
        return "\n" + itemDesc
    
    def getShortDescription(self):
        return self.desc + self.getItemDesc() 

    def getLongDescription(self):
        return self.longDesc + self.getItemDesc()
rooms = {
    "reaper" : Room("Reaper's Place","Long desc"),
    "reaper_basement": Room("Reaper's Basement","Long desc")
}

rooms["reaper_basement"].items[docsCyberdeck.name] = docsCyberdeck
rooms['reaper'].down = rooms['reaper_basement']
rooms['reaper_basement'].up = rooms['reaper']
currentRoom = rooms['reaper']

def clear():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')

def animPrint(msg):
    for char in msg:
        if char == ".":
            time.sleep(textAnimSpeed*10)
        print(char, end='', flush=True)
        time.sleep(textAnimSpeed)
def processUserInput(userInput):
    parse = userInput.split(' ')
    if(commands.get(parse[0]) and commands.get(parse[0])['access'] <= player["Character"].accessLevel):
        if(len(parse) > 1):
            commands[parse[0]]['func'](parse[1:])
        else:
            commands[parse[0]]['func'](parse[0])
        return 0
    elif(len(parse[0]) == 0):
        return 0
    return 1

def gameLoop():
    global currentState
    global promptUser
    global currentPrompt
    global player
    while gameRunning:
        if promptUser:
            resp = input(currentPrompt)
            status = processUserInput(resp)    # 0 means OK 1 means FAILED
        else:
            clear()
            
        match currentState:
            case States.MAIN_MENU:
                match resp:
                    case "1":
                        currentState = States.NIGHT_CITY
                        promptUser = False
                    case "2":
                        print("Config");
                    case "3":
                        print("Credits");
                    case "4":
                        print("Quit");
            case States.NIGHT_CITY:
                animPrint("You've finally made it, well sort of. You've reached the famous Night City - a site to behold, a bit different than you're accustomed to, but you've ran out of options. You were made an outcast by your group and after months of scraping by you've finally managed to afford a cheap apartment. Your rent's due by the end of the month and your running low on cash. While crashing at home for the night sounds like heaven, it would be  best to go see a ripperdoc you'll need a cheap cyberdeck if you expect to live out here and netrunning is all you know.\n\n\n\n")
                currentPrompt = "Press Enter To Continue"
                promptUser = True
                currentState = States.RIPPER_DOC
            case States.RIPPER_DOC:
                if not player["Character"].name:
                    clear()
                    animPrint("You decide to take a stroll through the district and after a few hours getting acquanted you've gathered that if your looking for quantity, you need to see the doc known as 'The Reaper'. He's known to carry unique hardware and can handle most implants no questions asked. You decide this is the best bet.\nYou arrive at The Reaper's spot - its a pretty unassuming building and isn't visibly marked. You take a beat before reaching for the door. Just as you do the door swings open. 'COME ON NOW I AIN'T GOT ALL DAY' you hear someone shout from the inside. You startle just for a moment before taking a look inside the building. It's dark but you see some dim red lights marking a path down some stairs.\nYou don't waste any time and begin following the path.\nAs you do, you hear the same voice from earlier. The voice is softer now - a low almost calming tone.\n\n'Ahh another runner; not many of us left around here. Don't bother looking for me, I'm out at the moment. What's your name kid? ")
                    currentPrompt = "\nName? "
                    promptUser = True
                    player["Character"].name = "?"
                elif(player["Character"].name == "?"):
                    player["Character"].name = resp
                    resp = None
                    animPrint(player["Character"].name + " Huh? Looks like your a real nobody kid, but hey that's not the worse thing. Just looking at ya I can tell you don't have any money. Hell I almost pity you. I'll tell you what, since I'm out right now, how about you run the shop for a bit?'\n...'Alrighty then keep heading down to the basement, once you're there go ahead and get setup on my rig. I'll explain the rest once you're in.")
                    print("\n\n\n\nYou can now use basic movement commands. Use the help command for more info.")
                    currentPrompt = "Press Enter To Continue"
                else:
                    promptUser = False
                    currentState = States.MEAT_SPACE
                    player["Character"].accessLevel = 1
                    print("\n")
                    clear()
            case States.MEAT_SPACE:
                promptUser = True
                currentPrompt = f"[{player['Character'].name}]: "
                if(resp is None or status == 0):
                    if(currentRoom.visited):
                        print(currentRoom.getShortDescription())
                    else:
                        print(currentRoom.getLongDescription())
                elif(status == 1):
                    animPrint("You can't do that here!")
                currentRoom.visited = True                 
def addCommand(name, func, desc=""):
    global commands
    commands[name] = {
        "func": func,
        "access": 1,
        "description": desc
    }

def take(args):
    itemName = " ".join(args)
    if(itemName in currentRoom.items):
        inventory[itemName] = currentRoom.items[itemName]
        del currentRoom.items[itemName]
        print("\nYou take the " + itemName)

def use(args):
    itemName = " ".join(args)
    if(itemName in currentRoom.items):
        currentRoom.items[itemName].func()
    elif(itemName in inventory):
        inventory[itemName].func()
        
def look(args):
    print(currentRoom.longDesc)

def move(direction):
    global currentRoom
    match direction:
        case "up":
            currentRoom = currentRoom.up or currentRoom
            return 1
        case "down":
            currentRoom = currentRoom.down or currentRoom
            return 1
        case "n":
            currentRoom = currentRoom.n or currentRoom
            return 1
        case "ne":
            currentRoom = currentRoom.ne or currentRoom
            return 1
        case "e":
            currentRoom = currentRoom.e or currentRoom
            return 1
        case "se":
            currentRoom = currentRoom.se or currentRoom
            return 1
        case "s":
            currentRoom = currentRoom.s or currentRoom
            return 1
        case "sw":
            currentRoom = currentRoom.sw or currentRoom
            return 1
        case "w":
            currentRoom = currentRoom.w or currentRoom
            return 1
        case "nw":
            currentRoom = currentRoom.nw or currentRoom
        case "_":
            return 1
    return 0

def dispHelp(args):
    print("---RTFMan---")
    for name in commands:
        print(f"{name} - {commands[name]['description']}")

def registerCommands():
    addCommand('up',move,"Move up")
    addCommand('down',move, "Move down")
    addCommand('n',move, "Move north")
    addCommand('ne',move, "Move north-east")
    addCommand('e',move, "Move east")
    addCommand('se',move, "Move south-east")
    addCommand('s',move, "Move south")
    addCommand('sw',move, "Move south-west")
    addCommand('w',move, "Move west")
    addCommand('nw',move, "Move north-west")
    addCommand('take', take, "Take an item from the room you're in")
    addCommand('use', use, "Use an item in the room or in your inventory")
    addCommand('look', look, "Look around the room you're in")
    addCommand('help',dispHelp, "What do you think?")
def main():
    clear()
    registerCommands()
    logo = r"""
   _____      _                                 _               
  / ____|    | |                               | |              
 | |    _   _| |__   ___ _ __ _ __  _   _ _ __ | | __           
 | |   | | | | '_ \ / _ \ '__| '_ \| | | | '_ \| |/ /           
 | |___| |_| | |_) |  __/ |  | |_) | |_| | | | |   <            
  \_____\__, |_.__/ \___|_|  | .__/ \__,_|_| |_|_|\_\           
         __/ |               | |             
       _|___/   ___        _ |_|___      _____    ____        _ 
      / ____|  / _ \      | | |___ \    |  __ \  |___ \      | |
     | |      | | | |   __| |   __) |   | |__) |   __) |   __| |
     | |      | | | |  / _` |  |__ <    |  _  /   |__ <   / _` |
     | |____  | |_| | | (_| |  ___) |   | | \ \   ___) | | (_| |
      \_____|  \___/   \__,_| |____/    |_|  \_\ |____/   \__,_|
                                                                
                                                                
    """
    animPrint(logo);
    print('\n')
    animPrint('\t\t<===|NETRUNNER] - [C0d3 Z3r0|===>\n\n\t\t\t-Written by Rake\n\n\n');
    print('\t\t\t  --MAIN MENU--\n')
    print('\t\t\t   1) Start Game')
    print('\t\t\t   2) Config')
    print('\t\t\t   3) Credits')
    print('\t\t\t   4) Quit\n\n')
    global currentPrompt
    currentPrompt = "Select an option:"
    gameLoop();

    
if __name__ == '__main__':
    main()
