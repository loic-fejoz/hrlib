# -*- coding: latin1 -*-
import Item
import sets
class Place(Item.Item):

    id = None
    creationDate = 0
    modificationDate = 0
    mainPlaceID = 0
    town = u''
    code = u''
    department = u''
    region = u''
    country = u''
    
    def __init__(self):
        self.linkMedias = sets.Set()
        
    def __str__(self):
        return u"%s, %s, %s, %s, %s" % (self.town,self.code,self.department,self.region,self.country)
