# -*- coding: latin-1 -*-
"""
The base class for all HeredisFile.
You should only call the open function.

GPL Copyright (C) 2004  Loïc Fejoz
"""
import unpack
import os
import types
import FileProxy

def getObjectsClassDict():
    import Objects
    return Objects.objects

def open(fileName=None, objectsClassDict=None, HeredisFileClass=None, openedFile=None, stopOnError=True, tablesToRecover=None):
    """ return an HeredisFile object of the given fileName"""
    if not objectsClassDict:
        objectsClassDict = getObjectsClassDict()
    if not HeredisFileClass:
        HeredisFileClass = HeredisFile
    return HeredisFileClass(fileName, objectsClassDict, openedFile, stopOnError, tablesToRecover)

class HeredisFile(object):
    """
    An HeredisFile only generates elements from an Heredis File.
    """
    def  __init__(self,fileName=None, objectsClassDict=None, openedFile=None, stopOnError=True, tablesToRecover=None):
        if fileName:
            self.fileName = fileName
        else:
            self.fileName = "NoName"
        if objectsClassDict:
            self._objectsClass = objectsClassDict
        else:
            self._objectsClass = getObjectsClassDict()
        self._file = openedFile
        fh = self._objectsClass['FileHeader']
        self.fileHeader = unpack.getFileHeader(self, fh)
        tableHeaders = {}
        for h in self.tableHeaderGenerator():
            tableHeaders[h.name]=h
        self.tableHeaders = tableHeaders
        if tablesToRecover:
            self.tablesToRecover = tablesToRecover
        else:
            self.tablesToRecover = {}
        self.stopOnError = stopOnError

    itemGenerator = unpack.itemGenerator

    itemSizeGenerator = unpack.itemSizeGenerator

    def fdopen(self):
        if not self._file:
            return file(self.fileName, "rb")
#            self._file = file(self.fileName, "rb")
        return FileProxy.FileProxy(self._file)
##        try:
##            fno = self._file.fileno()
##            fd = os.fdopen(fno)
##            return fd
##        except:
##            print "yop"
##            return file(self.fileName, "rb")
        
    def close(self):
        if self._file:
            self._file.close()
            self._file = None
        del self.tableHeaders

    def tableHeaderGenerator(self):
        return iter(unpack.tableHeaderGenerator(self,self._objectsClass['TableHeader']))
            
    def individuGenerator(self):
        return iter(self.itemGenerator('TH5TableIndividus',
                                       unpack.unpackIndividu,
                                       self._objectsClass['Individu']))
        
    def surnameGenerator(self):
        return iter(self.itemGenerator('TH5TableDicoNoms',
                                          unpack.unpackSurname,
                                          self._objectsClass['Surname']))
            
    def unionGenerator(self):
        return iter(self.itemGenerator('TH5TableUnion',
                                        unpack.unpackUnion,
                                        self._objectsClass['Union']))

    def eventGenerator(self):
        return iter(self.itemGenerator('TH5TableEvenements',
                                        unpack.unpackEvent,
                                        self._objectsClass['Event']))
            
    def placeGenerator(self):
        return iter(self.itemGenerator('TH5TableDicoLieux',
                                        unpack.unpackPlace,
                                        self._objectsClass['Place']))

    def addressGenerator(self):
        if False: #self.fileHeader.software_version < 6:
            tableName = 'TH5TableDicoAddresses'
        else:
            tableName = 'TH5TableDicoAdresses'
        return iter(self.itemGenerator(tableName,
                                       unpack.unpackAddresse,
                                       self._objectsClass['Address']))
            
    def sourceGenerator(self):
        return iter(self.itemGenerator('TH5Doc',
                                         unpack.unpackSource,
                                         self._objectsClass['Source']))
            
    def mediaGenerator(self):
        return iter(self.itemGenerator('TH5TableMedias',
                                        unpack.unpackMedia,
                                        self._objectsClass['Media']))
            
    def linkGenerator(self):
        return iter(self.itemGenerator('TBLINK',
                                       unpack.unpackLink,
                                       self._objectsClass['Link']))
            
    def linkDocGenerator(self):
        return iter(self.itemGenerator('TH5LinkDoc',
                                          unpack.unpackLinkDoc,
                                          self._objectsClass['LinkDoc']))
            
    def linkMediaGenerator(self):
        return iter(self.itemGenerator('TBMedia-IdxOwner',
                                            unpack.unpackLinkMedia,
                                            self._objectsClass['LinkMedia']))
    
