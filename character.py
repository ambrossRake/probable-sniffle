class Character:

    def __init__(self,currentRoom, name = "", age = 0, eddies = 0, reputation = 0, inventory = {}, accessLevel = 0):
        self.name = name
        self.age = age
        self.eddies = eddies
        self.reputation = reputation
        self.inventory = inventory
        self.accessLevel = accessLevel
        self.currentRoom = currentRoom
