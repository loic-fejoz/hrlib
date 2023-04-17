# -*- coding: latin1 -*-

import Item

class Link(Item.Item):
    linkTypes = {1:u'Aïeul(e) -> Descendant(e)',
                 2:u'Ami(e) -> Ami(e)',
                 3:u'Beau-frère/Belle-soeur -> Beau-frère/Belle-soeur',
                 4:u'Beau-père/Belle-mère -> Gendre/Bru',
                 5:u'Lien consanguin',
                 6:u'Cousin/Cousine -> Cousin/Cousine',
                 7:u'Doublon ? -> Doublon ?',
                 8:u'Frère/Soeur -> Frère/Soeur',
                 9:u'Jumeau/Jumelle -> Jumeau/Jumelle',
                 10:u'Testateur/Testatrice -> Héritier/Héritière',
                 11:u'Oncle/Tante -> Neveu/Nièce',
                 12:u'Parent(e) -> Parent(e)',
                 13:u'A reconnu -> Reconnu par',
                 14:u'Tuteur/Tutrice -> Sous tutelle',
                 15:u'Autre Lien',
                 #16
                 17:u'Déclarant',
                 18:u"Officier d'état civil",
                 19:u'Officiant Religieux',
                 20:u'Parrain/Marraine',
                 21:u'Présent(e)',
                 22:u'Témoin',
                 23:u'Autre Lien'}

    id = None
    creationDate = 0
    modificationDate = 0
    fromItemID = None
    toItemID = None
    note = u''
    typeIndex = 15

    def getType(self):
        return self.linkTypes.get(self.typeIndex,str(self.typeIndex))

    type = property(getType)
