# -*- coding: latin1 -*-
"""
This module contain all the functions needed to decode an heredis file.
It is mainly use by the HeredisFile class.
See the Heredis format description...

GPL Copyright (C) 2004  Loïc Fejoz
"""
import logging
logger = logging.getLogger('hrlib.unpack')
import struct
import Buffer
import RawDataHelper

from HeredisError import HeredisError

def packFileHeader(fileHeader):
    """return the file header pack"""
    buffer = '\0' * 2380
    buffer = RawDataHelper.set('<4s',buffer,0,'\xC0\xDE\xCA\xFE')
    buffer = RawDataHelper.set('<23s',buffer,8,'Heredis\x99 6 for Windows\x99')
    buffer = RawDataHelper.set('<3s',buffer,0x29,'\x05\xDE\xFA')
    buffer = RawDataHelper.set('<4s',buffer,0x924,'\x10\x01\x00\x20')
    buffer = RawDataHelper.set('<32s',buffer,0x7C,fileHeader.name.encode('latin1'))
    buffer = RawDataHelper.set('<255s',buffer,0x9C,fileHeader.comment.encode('latin1'))
    buffer = RawDataHelper.set('<32s',buffer,0x92C,fileHeader.version.encode('latin1'))
    buffer = RawDataHelper.set('<l',buffer,0x4C,fileHeader.lastId)
    index = 0x19C
    for i  in  range(10):
        buffer = RawDataHelper.set('<64s',buffer,index, struct.pack('<32s32s',
                                                           fileHeader.userFields[i][0].encode('latin1'),
                                                           fileHeader.userFields[i][1].encode('latin1')))
        index = index + 64
    return buffer

def packTableHeader(name, itemSize, nbItem, tableSize):
    code = '\xC0\xDE\xCA\xFE'
    itemSize = '%011d\0' % itemSize
    nbItem = '%011d\0' % nbItem
    tableSize = '%011d\0' % tableSize
    return struct.pack("<4s40s12s12s12s", code, name, itemSize, nbItem, tableSize)

def packIndividu(result):
    buffer = Buffer.Buffer()
    buffer.set('<I',result.id)
    buffer.set('<I',result.creationDate)
    buffer.set('<I',result.modificationDate)
    buffer.set('<I',result.fatherID)
    buffer.set('<I',result.motherID)
    buffer.set('<I',result.surnameID)
    buffer.set('<I',result.unknown1)
    buffer.setString(result.name)
    buffer.setString(result.activity)
    buffer.setString(result.sex)
    buffer.setString(result.note)
    buffer.setString(result.numero)
    for i in range(10):
        buffer.setString(result.userFields[i])
    buffer.set('<H',result.unknown2)
    buffer.set('<H',result.sansDesc)
    buffer.set('<B',result.signatureIndex)
    buffer.set('<B',result.enfantIndex)
    buffer.set('<B',result.marque)
    buffer.set('<B',result.unknown3)
    buffer.set('<B',result.confidentiel)
    buffer.setString(result.suffixe)
    buffer.setString(result.surnom)
    buffer.setString(result.titre)
    buffer.addDummy(3)
    return buffer.buffer

def packSurname(result):
    buffer = Buffer.Buffer()
    buffer.set('<I',result.id)
    buffer.set('<I',result.creationDate)
    buffer.set('<I',result.modificationDate)
    buffer.set('<I',result.mainSurnameID)
    buffer.setString(result.name)
    buffer.addDummy(2)
    return buffer.buffer

def packUnion(result):
    buffer = Buffer.Buffer()
    buffer.set('<I',result.id)
    buffer.set('<I',result.creationDate)
    buffer.set('<I',result.modificationDate)
    buffer.set('<I',result.husbandID)
    buffer.set('<I',result.wifeID)
    buffer.set('<I',result.unknown1)
    buffer.setString(result.note)
    buffer.addDummy(b=(22-len(result.note)))
    return buffer.buffer

def packEvent(result):
    buffer = Buffer.Buffer()
    buffer.set('<I',result.id)
    buffer.set('<I',result.creationDate)
    buffer.set('<I',result.modificationDate)
    buffer.set('<I',result.itemID)
    buffer.set('<B',result.type)
    buffer.set('<I',result.placeID)
    buffer.set('<B',result.unknown1)
    buffer.set('<B',result.calendar1)
    buffer.set('<B',result.calendar2)
    buffer.set('<B',result.modif1)
    buffer.set('<B',result.modif2)
    buffer.set('<B',result.day1)
    buffer.set('<B',result.day2)
    buffer.set('<B',result.month1)
    buffer.set('<B',result.month2)
    buffer.set('<B',result.modif3)
    buffer.set('<B',result.partYear1)
    buffer.set('<B',result.selectYear1)
    buffer.set('<B',result.partYear2)
    buffer.set('<B',result.selectYear2)
    buffer.set('<B',result.hour)
    buffer.set('<B',result.minute)
    buffer.addDummy(format='<16B') # buffer.set('<16B',result.unknown2)
    buffer.setString(result.note)
    buffer.setString(result.placeSubdivision)
    buffer.setString(result.name)
    buffer.set('<H',result.unknown3)
    buffer.setString(result.ageOnAct)
    buffer.set('<B',result.findTheSource)
    buffer.addDummy(b=2)
    return buffer.buffer

def packPlace(result):
    buffer = Buffer.Buffer()
    buffer.set('<I',result.id)
    buffer.set('<I',result.creationDate)
    buffer.set('<I',result.modificationDate)
    buffer.set('<I',result.mainPlaceID)
    buffer.setString(result.town)
    buffer.setString(result.code)
    buffer.setString(result.department)
    buffer.setString(result.region)
    buffer.setString(result.country)
    buffer.addDummy(b=6)
    return buffer.buffer

def packAddresse(result):
    buffer = Buffer.Buffer()
    buffer.set('<I',result.id)
    buffer.set('<I',result.creationDate)
    buffer.set('<I',result.modificationDate)
    buffer.set('<I',result.unionID)
    buffer.set('<I',result.husbandID)
    buffer.set('<I',result.wifeID)
    buffer.set('<H',result.private)
    buffer.set('<B',result.unknown1)
    buffer.setString(result.contact)
    buffer.setString(result.line1)
    buffer.setString(result.line2)
    buffer.setString(result.postalCode)
    buffer.setString(result.town)
    buffer.setString(result.country)
    buffer.setString(result.phone)
    buffer.setString(result.fax)
    buffer.setString(result.email)
    buffer.setString(result.region)
    return buffer.buffer

def packSource(result):
    buffer = Buffer.Buffer()
    buffer.set('<I',result.id)
    buffer.set('<I',result.creationDate)
    buffer.set('<I',result.modificationDate)
    buffer.set('<B',result.unknown1)
    buffer.setString(result.origin)
    buffer.setString(result.document)
    buffer.setString(result.cote)
    buffer.setString(result.archivage)
    buffer.set('<H',result.type)
    buffer.set('<H',result.unknown2)
    buffer.setString(result.note)
    buffer.setString(result.name)
    return buffer.buffer

def packMedia(result):
    buffer = Buffer.Buffer()
    buffer.set('<I',result.id)
    buffer.set('<I',result.creationDate)
    buffer.set('<I',result.modificationDate)
    buffer.setString(result.directory)
    buffer.setString(result.fileName)
    buffer.set('<B',result.unknown1)
    buffer.setString(result.comment)
    buffer.set('<I',result.thumbnailLength)
    buffer.set('<B',result.year1)
    buffer.set('b',result.year2)
    buffer.set('<H',result.unknown2)
    buffer.set('<H',result.unknown3)
    buffer.addRaw(result.thumbnail)
    return buffer.buffer

def packLink(result):
    buffer = Buffer.Buffer()
    buffer.set('<I',result.id)
    buffer.set('<I',result.creationDate)
    buffer.set('<I',result.modificationDate)
    buffer.set('<I',result.fromItemID)
    buffer.set('<I',result.toItemID)
    buffer.setString(result.note)
    buffer.set('<H',result.unknown1)
    buffer.set('<B',result.typeIndex)
    return buffer.buffer

def packLinkDoc(result):
    buffer = Buffer.Buffer()
    buffer.set('<I',result.id)
    buffer.set('<I',result.creationDate)
    buffer.set('<I',result.modificationDate)
    buffer.set('<I',result.evtID)
    buffer.set('<I',result.sourceID)
    buffer.setString(result.note)
    return buffer.buffer

def packLinkMedia(result):
    buffer = Buffer.Buffer()
    buffer.set('<I',result.id)
    buffer.set('<I',result.creationDate)
    buffer.set('<I',result.modificationDate)
    buffer.set('<I',result.ownerID)
    buffer.set('<I',result.mediaID)
    buffer.set('<I',result.mainMedia)
    return buffer.buffer
