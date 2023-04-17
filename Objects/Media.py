import Item
import sets

class Media(Item.Item):
    
    id = None
    creationDate = 0
    modificationDate = 0
    directory = u''
    fileName = u''
    comment = u''
    thumbnailLength = 0
    year1 = 0               #sert au calcul de self.year
    year2 = 0               #sert au calcul de self.year
    thumbnail = ''          # image au format jpeg
    
    def __init__(self):
        self.events = sets.Set()
        self.linkMedias = sets.Set()
        self.links = sets.Set()
        self.reverseLinks = sets.Set()

    def getYear(self):
        return 256 * self.year2 + self.year1

    def setYear(self,year):
        self.year2 = int(year/256)
        self.year1 = int(year) - self.year2 * 256

    year = property(getYear,setYear,doc="year of the media")
