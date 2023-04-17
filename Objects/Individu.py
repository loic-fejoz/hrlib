# -*- coding: latin-1 -*-

import Item
import sets

class Individu(Item.Item):
    signatureDict = {0:u'Signe peut-etre',
                     1:u'Sait signer',
                     2:u'Ne signe pas'}

    enfantDict = {0:u'enfant legitime',
                  1:u'enfant naturel',
                  2:u'enfant reconnu',
                  3:u'enfant legitime',
                  4:u'enfant trouve',
                  5:u'enfant adopte',
                  6:u'enfant adulterin',
                  7:u'enfant mort-ne',
                  8:u'filiation non connue'}

    id = None
    creationDate = 0
    modificationDate = 0
    fatherID = None
    motherID = None
    surnameID = None
    name = None
    activity = None
    sex = u'?'
    note = u''
    numero = u''
    userFields = None
    sansDesc = None
    signatureIndex = 0
    enfantIndex = 0
    marque = False
    confidentiel = False
    suffixe = u''
    surnom = u''
    titre = u''
    
    def __init__(self):
        self.events = sets.Set()
        self.unions = sets.Set()
        self.addresses = sets.Set()
        self.links = sets.Set()
        self.linkMedias = sets.Set()
        self.reverseLinks = sets.Set()
        self.userFields = [None] * 11
        self.children = sets.Set()

    def getFamily(self):
        if self.father and self.mother:
            unions = [union for union in self.father.unions if union in self.mother.unions]
            for union in unions:
                self.__dict__['family'] = union
                return union
            else:
                self.__dict__['family'] = None
		
    family = property(getFamily)

    def getFullName(self):
        if hasattr(self, "surname"):
            surname = self.surname.name
        else:
            surname = unicode(self.surnameID)
        return "%s %s" % (self.name, surname)
    
    fullName = property(getFullName,doc="name + surname")

    def getSignature(self):
        return self.signatureDict[self.signatureIndex]

    signature = property(getSignature,"does he know how to sign ?")

    def getEnfant(self):
        return self.enfantDict[self.enfantIndex]

    enfant = property(getEnfant,doc="type of child")
