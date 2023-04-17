import Item
import sets

class Union(Item.Item):

    id = None
    creationDate = 0
    modificationDate = 0
    husbandID = None
    wifeID = None
    note = u''
    
    def __init__(self):
        self.events = sets.Set()
        self.links = sets.Set()
        self.reverseLinks = sets.Set()
        self.children = sets.Set()
        self.linkMedias = sets.Set()
        self.addresses = sets.Set()

    def getFullName(self):
        return "%s x %s" % (self.husband.fullName,self.wife.fullName)
    
    fullName = property(getFullName,doc="a description of the union")

    def getSpouse(self,indi):
        if indi == self.wife:
            return self.husband
        elif indi == self.husband:
            return self.wife
        else:
            return None
