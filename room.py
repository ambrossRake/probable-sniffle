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
