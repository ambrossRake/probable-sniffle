
class Item:
    def __init__(self, name, desc, func):
        self.name = name
        self.desc = desc
        self.func = func

    def use(self,params):
        self.func(params)
