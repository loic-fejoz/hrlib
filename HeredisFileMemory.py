# -*- coding: latin-1 -*-
"""
An HeredisFile that load every object in the memory.
You should only call the open function.

GPL Copyright (C) 2004  Loïc Fejoz
"""
import logging
logger = logging.getLogger('hrlib.HeredisFileMemory')
import HeredisFile

def open(fileName=None, objectsClass = None, openedFile=None, stopOnError=True, tablesToRecover=None):
    """ return an HeredisFile object for the given fileName"""
    return HeredisFile.open(fileName, objectsClass, HeredisFileMemory, openedFile, stopOnError, tablesToRecover)

def getType(obj):
    if obj:
        return obj.getType()
    return 'None'

def getID(obj):
    if obj:
        return obj.id
    return 'NoId'

class HeredisFileMemory(HeredisFile.HeredisFile):
    """ It loads all data in dictionary and link them together.
    Suppose h to be an HeredisFileMemory instance.
    You can access data trough h[tableName] which is again a dictionary. Keys are identifier.
    For example, all individus are in h['individus'].
    You can also retrieve item by id by looking for the id in h['ids'].
    """
    def __init__(self,fileName=None, objectsClassDict=None, openedFile=None, stopOnError=True, tablesToRecover=None):
        super(HeredisFileMemory, self).__init__(fileName, objectsClassDict, openedFile, stopOnError, tablesToRecover)
        self._data = {}
        self._loadData()

    def close(self):
        del self._data
        super(HeredisFileMemory, self).close()

    def __getitem__(self,tableName):
        return self._data[tableName]

    def _loadData(self):
        data = self._data
        data['ids'] = {}
        self._loadDataFromTable(self.individuGenerator,"individus")
        self._loadDataFromTable(self.surnameGenerator,"surnames")
        self._loadDataFromTable(self.unionGenerator,"unions")
        self._loadDataFromTable(self.eventGenerator,"events")
        self._loadDataFromTable(self.placeGenerator,"places")
        self._loadDataFromTable(self.addressGenerator,"addresses")
        self._loadDataFromTable(self.sourceGenerator,"sources")
        self._loadDataFromTable(self.mediaGenerator,"medias")
        self._loadDataFromTable(self.linkGenerator,"links")
        self._loadDataFromTable(self.linkDocGenerator,"linkDocs")
        self._loadDataFromTable(self.linkMediaGenerator,"linkMedias")
        self._addOtherData()
        self._redefineFunctions()

    def _loadDataFromTable(self,generator,tableName):
        logger.info('loading data from table %s',tableName)
        data = self._data
        table = data[tableName] = {}
        ids = data['ids']
        i = 1
        for  obj in generator():
            id = obj.id
            oldObj = ids.get(id,None)
            if oldObj:
                logger.warning("two objects have the same id ! %s and %s have %s",oldObj.getType(),obj.getType(),id)
            ids[id] = table[id] = obj
            i+=1
        logger.info('%d items loaded',i)

    def _addOtherData(self):
        data = self._data
        indis = data['individus']
        surnames = data['surnames']
        ids = data['ids']
        places = data['places']
        unions = data['unions']
        surnames = data['surnames']
        events = data['events']
        addresses = data['addresses']
        links = data['links']
        linkDocs = data['linkDocs']
        linkMedias = data['linkMedias']
        sources = data['sources']
        medias = data['medias']
        # set surname,father,mother for indi
        for indi in indis.itervalues():
            indi.surname = surnames.get(indi.surnameID,None)
            indi.father = indis.get(indi.fatherID,None)
            indi.mother = indis.get(indi.motherID,None)
        # add mainSurname to surname
        for surname in surnames.itervalues():
            surname.mainSurname = ids[surname.mainSurnameID]
        # add union to indi
        familyDico = {}
        for union in unions.itervalues():
            husband = union.husband = indis.get(union.husbandID,None)
            wife = union.wife = indis.get(union.wifeID,None)
            if husband:
                husband.unions.add(union)
            else:
                logger.warning("Missing husband in union %s", union.id)
            if wife:
                wife.unions.add(union)
            else:
                logger.warning("Missing wife in union %s", union.id)
            if wife and husband:
                familyDico[(husband.id, wife.id)] = union
        # add children of union
        for indi in indis.itervalues():
            family = familyDico.get((indi.fatherID,indi.motherID),None)
            if family:
                family.children.add(indi)
            if indi.fatherID:
                if indi.father:
                    indi.father.children.add(indi)
                else:
                    logger.warning("Cannot add child to father %d", indi.fatherID)
            if indi.motherID:
                if indi.mother:
                    indi.mother.children.add(indi)
                else:
                    logger.warning("Cannot add child to mother %d", indi.motherID)
        # add events to their respective items
        # set event place
        for evt in events.itervalues():
            # sometime an id appear twice... :-(
            #obj = evt.item = ids[evt.itemID]
            obj = evt.item = indis.get(evt.itemID,None) or unions.get(evt.itemID,None) or ids.get(evt.itemID,None)
            if hasattr(obj,"events"):
                obj.events.add(evt)
            else:
                logger.warning("%s(%s) has no events attr but has events %s(%s) of type %s attached !",getType(obj),getID(obj),getType(evt),getID(evt),evt.typeName)
            evt.place = places.get(evt.placeID,None)
        # set mainPlace
        for place in places.itervalues():
            place.mainPlace = places.get(place.mainPlaceID,None)
        # set addresse
        for addresse in addresses.itervalues():
            husband = addresse.husband = indis.get(addresse.husbandID,None)
            wife = addresse.wife = indis.get(addresse.wifeID,None)
            union = addresse.union = unions.get(addresse.unionID,None)
            if husband:
                husband.addresses.add(addresse)
            if wife:
                wife.addresses.add(addresse)
            if union:
                union.addresses.add(addresse)
        # links
        for link in links.itervalues():
            # problem sometime there are sime id twice...
            #fromItem = link.fromItem = ids[link.fromItemID]
            #toItem = link.toItem = ids[link.toItemID]
            fromItem = link.fromItem = indis.get(link.fromItemID,None) or events.get(link.fromItemID,None) or unions(link.fromItemID,None) or ids.get(link.fromItemID,None)
            toItem = link.toItem = indis.get(link.toItemID,None) or ids.get(link.toItemID,None)
            if hasattr(fromItem,'links'):
                fromItem.links.add(link)
            else:
                logger.warning("%s(%d) has no attr 'links' but has link attached : %s(%d) of type %s",getType(fromItem),getID(fromItem),getType(link),getID(link),link.type)
            if hasattr(toItem,'reverseLinks'):
                toItem.reverseLinks.add(link)
        # linkDoc
        for linkDoc in linkDocs.itervalues():
            event = linkDoc.event = events.get(linkDoc.evtID,None) or ids.get(linkDoc.evtID,None)
            source = linkDoc.source = sources.get(linkDoc.sourceID,None) or ids.get(linkDoc.sourceID,None)
            source.linkDocs.add(linkDoc)
            event.linkDocs.add(linkDoc)
        # linkMedia
        for linkMedia in linkMedias.itervalues():
            owner = linkMedia.owner = indis.get(linkMedia.ownerID,None)\
                    or sources.get(linkMedia.ownerID,None)\
                    or ids.get(linkMedia.ownerID,None)
            media = linkMedia.media = medias.get(linkMedia.mediaID,None) or ids.get(linkMedia.mediaID,None)
            if hasattr(owner,'linkMedias'):
                owner.linkMedias.add(linkMedia)
            if hasattr(media,'linkMedias'):
                media.linkMedias.add(linkMedia)

    def _redefineFunctions(self):
        self.individuGenerator = lambda: iter(self._data['individus'].itervalues())
        self.surnameGenerator = lambda: iter(self._data['surnames'].itervalues())
        self.unionGenerator = lambda: iter(self._data['unions'].itervalues())
        self.eventGenerator = lambda: iter(self._data['events'].itervalues())
        self.placeGenerator = lambda: iter(self._data['places'].itervalues())
        self.addresseGenerator = lambda: iter(self._data['addresses'].itervalues())
        self.sourceGenerator = lambda: iter(self._data['sources'].itervalues())
        self.mediaGenerator = lambda: iter(self._data['medias'].itervalues())
        self.linkGenerator = lambda: iter(self._data['links'].itervalues())
        self.linkDocGenerator = lambda: iter(self._data['linkDocs'].itervalues())
        self.linkMediaGenerator = lambda: iter(self._data['linkMedias'].itervalues())
        
