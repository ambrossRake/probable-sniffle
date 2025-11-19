import os
import time

gameRunning = True;
commands = {};
currentPrompt = "";
name = "";
age = 0;
eddies = 0;
rep = 0;
currentState = "main_menu"
lastState = currentState
promptUser = True
inventory = {}

class Item:
    def __init__(self, name, desc, func):
        self.name = name
        self.desc = desc
        self.func = func

    def use(self,params):
        self.func(params)

docsCyberdeck = Item("Old Cyberdeck", "An old cyberdeck", None)

class Room:
    def __init__(self, description):
        self.desc = description
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
        
    def getShortDescription(self):
        plural = ""
        if len(self.items) > 1:
            plural = "are"
        elif len(self.items) == 1:
            plural = "is"
        else:
            return self.desc
        
        itemDesc = f"There {plural} "
        for item in self.items:
            itemDesc += "a " + item
        return self.desc + "\n" + itemDesc
    
rooms = {
    "reaper" : Room("Reaper's Place"),
    "reaper_basement": Room("Reaper's Basement")
}

rooms["reaper_basement"].items[docsCyberdeck.name] = docsCyberdeck
rooms['reaper'].down = rooms['reaper_basement']
currentRoom = rooms['reaper']

def clear():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')

def processCommand(userInput):
    commands[userInput](userInput)

def animPrint(msg):
    for char in msg:
        if char == ".":
            time.sleep(.35)
        print(char+"", end='', flush=True)
        time.sleep(.02)
def processUserInput(userInput):
    if(commands.get(userInput)):
        commands[userInput]['func'](userInput)
        return 0
    return 1

def gameLoop():
    global currentState
    global promptUser
    global currentPrompt
    global name
    
    while gameRunning:
        if promptUser:
            resp = input(currentPrompt)
            status = processUserInput(resp)    # 0 means OK 1 means FAILED
        else:
            clear()
            
        match currentState:
            case "main_menu":
                match resp:
                    case "1":
                        currentState = "night_city"
                        promptUser = False
                    case "2":
                        print("Config");
                    case "3":
                        print("Credits");
                    case "4":
                        print("Quit");
            case "night_city":
                animPrint("You've finally made it, well sort of. You've reached the famous Night City - a site to behold, a bit different than you're accustomed to, but you've ran out of options. You were made an outcast by your group and after months of scraping by you've finally managed to afford a cheap apartment. Your rent's due by the end of the month and your running low on cash. While crashing at home for the night sounds like heaven, it would be  best to go see a ripperdoc you'll need a cheap cyberdeck if you expect to live out here and netrunning is all you know.\n\n\n\n")
                currentPrompt = "Press Enter To Continue"
                promptUser = True
                currentState = "ripperdoc"
            case "ripperdoc":
                if not name:
                    clear()
                    animPrint("You decide to take a stroll through the district and after a few hours getting acquanted you've gathered that if your looking for quantity, you need to see the doc known as 'The Reaper'. He's known to carry unique hardware and can handle most implants no questions asked. You decide this is the best bet.\nYou arrive at The Reaper's spot - its a pretty unassuming building and isn't visibly marked. You take a beat before reaching for the door. Just as you do the door swings open. 'COME ON NOW I AIN'T GOT ALL DAY' you hear someone shout from the inside. You startle just for a moment before taking a look inside the building. It's dark but you see some dim red lights marking a path down some stairs.\nYou don't waste any time and begin following the path.\nAs you do, you hear the same voice from earlier. The voice is softer now - a low almost calming tone.\n\n'Ahh another runner; not many of us left around here. Don't bother looking for me, I'm out at the moment. What's your name kid? ")
                    currentPrompt = "\nName? "
                    promptUser = True
                    name = "?"
                elif(name == "?"):
                    name = resp
                    resp = None
                    animPrint(name + " Huh? Looks like your a real nobody kid, but hey that's not the worse thing. Just looking at ya I can tell you don't have any money. Hell I almost pity you. I'll tell you what, since I'm out right now, how about you run the shop for a bit?'\n...'Alrighty then keep heading down to the basement, once you're there go ahead and get setup on my rig. I'll explain the rest once you're in.")
                    animPrint("\n\n\n\nYou can now use basic movement commands. Use the help command for more info.")
                    currentPrompt = "Press Enter To Continue"
                    promptUser = False
                else:
                    currentState = "meat_space"
                    clear()
            case "meat_space":
                promptUser = True
                currentPrompt = f"[{name}]: "
                if(resp is None or status == 0):
                    print(currentRoom.getShortDescription())
                elif(status == 1):
                    animPrint("You can't do that here!")                  
def addCommand(name, func, params):
    global commands
    commands[name] = {
        "func": func,
        "params": params,
        "access": 0
    }

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

def registerCommands():
    addCommand('up',move, "up")
    addCommand('down',move, "down")
    addCommand('n',move, "n")
    addCommand('ne',move, "ne")
    addCommand('e',move, "e")
    addCommand('se',move, "se")
    addCommand('s',move, "s")
    addCommand('sw',move, "sw")
    addCommand('w',move, "w")
    addCommand('nw',move, "nw")

def main():
    clear()
    registerCommands()
    logo = r"""
 _________        ___.                                     __       
 \_   ___ \___.__.\_ |__   _________________  __ __  ____ |  | __   
/    \  \<   |  | | __ \_/ __ \_  __ \____ \|  |  \/    \|  |/ /   
\     \___\___  | | \_\ \  ___/|  | \/  |_> >  |  /   |  \    <    
 \______  / ____| |___  /\___  >__|  |   __/|____/|___|  /__|_ \   
        \/\/          \/     \/      |__|              \/     \/   


_________ _______       .___________      __________________      .___
\_   ___ \\   _  \    __| _/\_____  \     \______   \_____  \   __| _/
/    \  \//  /_\  \  / __ |   _(__  <     |       _/ _(__  <  / __ | 
\     \___\  \_/   \/ /_/ |  /       \    |    |   \/       \/ /_/ | 
 \______  /\_____  /\____ | /______  /    |____|_  /______  /\____ | 
        \/       \/      \/        \/            \/       \/      \/"""
    print(logo);
    print('\nNetrunner - C0d3 Z3r0\n-By R4k3\n\n\n\n');
    print('---Main Menu---')
    print('1) Start Game')
    print('2) Config')
    print('3) Credits')
    print('4) Quit')
    global currentPrompt
    currentPrompt = "Select an option:"
    gameLoop();

    
if __name__ == '__main__':
    main()
