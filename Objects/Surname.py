import Item
import sets

class Surname(Item.Item):
    
    id = None
    creationDate = 0
    modificationDate = 0
    mainSurnameID = None
    name = u''
    
    def __init__(self):
        self.events = sets.Set()
