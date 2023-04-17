# -*- coding: latin1 -*-

import Item
import sets

class Source(Item.Item):
    natures = {0:u'non trouvé',
               1:u'original',
               2:u'copie',
               3:u'photocopie',
               4:u'transcription',
               5:u'numerisation',
               6:u'microfilm',
               7:u'demandé',
               8:u'extrait',
               9:u'photographie',
               10:u'introuvable',
               11:u'cdrom',
               12:u'audio',
               16:u'carte',
               17:u'journal',
               13:u'livre',
               14:u'magazine',
               15:u'manuscrit',
               18:u'pierre tombale',
               19:u'video',
               20:u'souvenir',
               21:u'internet'}


    id = None
    creationDate = 0
    modificationDate = 0
    origin = u''
    document = u''
    cote = u''
    archivage = u''
    type = u''
    note = u''
    name = u''

    def __init__(self):
        self.linkDocs = sets.Set()
        self.linkMedias = sets.Set()

    def getNature(self):
        return self.natures.get(self.type,str(self.type))

    nature = property(getNature)
