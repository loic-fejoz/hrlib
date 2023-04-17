# -*- coding: latin-1 -*-
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

def getFileHeader(heredisFile,fileHeaderClass):
    """return the file header"""
    fileHeader = fileHeaderClass()
    f = heredisFile.fdopen()
    header = f.read(2380)
    #f.close()
    (code,) = struct.unpack('<4s',header[:4])
    if code != '\xC0\xDE\xCA\xFE':
        logger.error("ceci n'est pas un fichier Heredis valide")
        logger.error(RawDataHelper.str2hex(code))
        raise ValueError,'Not a valid Heredis f'
    (fileHeader.unknown1,) = struct.unpack('<4s', header[4:8])
    logger.debug('unknown : %s',fileHeader.unknown1)
    (fileHeader.software,) = RawDataHelper.cString2String(RawDataHelper.get('<32s',header,0x8))
    fileHeader.software_version = int(fileHeader.software[8:11])
    (fileHeader.unknown2,) = RawDataHelper.get('<H',header,0x50)
    logger.debug('unknown : %s',fileHeader.unknown2)
    (fileHeader.name,) = RawDataHelper.cString2String(RawDataHelper.get('<32s',header,0x7C))
    (fileHeader.comment,) = RawDataHelper.cString2String(RawDataHelper.get('<255s',header,0x9C))
    (fileHeader.version,) = RawDataHelper.cString2String(RawDataHelper.get('<32s',header,0x92C))
    (fileHeader.versionComplete,) = RawDataHelper.cString2String(RawDataHelper.get('<32s',header,0x92C))
    logger.info(fileHeader.versionComplete)
    logger.info(RawDataHelper.str2hex(fileHeader.versionComplete))
    (fileHeader.lastId,) = RawDataHelper.get('<l',header,0x4C)
    index = 0x19C
    fileHeader.userFields = []
    for i  in  range(10):
        (attr,tag) = RawDataHelper.cString2String(struct.unpack('<32s32s',header[index:index+64]))
        fileHeader.userFields.append((attr,tag))
        index = index + 64
    return fileHeader

def findNextTable(inFile):
    """ this method is called on Error to find the next table if any."""
    waitingC0 = 1
    waitingDE = 2
    waitingCA = 3
    waitingFE = 4
    ok = 5
    state = waitingC0
    while state != ok:
        pos = inFile.tell()
        c = inFile.read()
        if c == '':
            return None
        if c == '\xC0':
            state = waitingDE
        elif state == waitingDE and c == '\xDE':
            state = waitingCA
        elif state == waitingCA and c == '\xCA':
            state = waitingFE
        elif state == waitingFE and c == '\xFE':
            state = ok
        else:
            state = waitingC0
    return pos

def tableHeaderGenerator(heredisFile,headerClass):
    f = heredisFile.fdopen()
    f.seek(2380) #skip the file header
    pos = f.tell()
    buffer = f.read(80)
    while buffer:
        (code,name,itemSize,nbItem,tableSize) = struct.unpack("<4s40s12s12s12s",buffer)
        rawName = name
        if code == '\xC0\xDE\xCA\xFE':
            # ok a new table header was found
            try:
                itemSize = int(itemSize[:-1])
                nbItem = int(nbItem[:-1])
                tableSize = int(tableSize[:-1])
            except:
                logger.exception('invalid table header at position 0x%x: %s' %(pos,(code,name,itemSize,nbItem,tableSize)))
            try:
                name = RawDataHelper.cString2String(name)
            except:
                logger.exception('invalid table name at position 0x%x: %s' %(pos,(code,name,itemSize,nbItem,tableSize)))
                name = RawDataHelper.str2hex(name)
                # raise HeredisError,"Entete de table invalide"
        else:
            # This is not a table header but...
            if heredisFile.fileHeader.software_version < 6:
                # an error !
                logger.warning("The file is severously endommaged! Trying to recover")
                previousPos = pos
                pos = findNextTable(f)
                if pos:
                    logger.warning('Table header found at position 0x%x' % pos)
                    f.seek(pos, 0)
                    buffer = f.read(80)
                    continue
                else:
                    logger.critical('Unable to recover from invalid table header at 0x%x!' % previousPos)
                    buffer = None
                    continue
                logger.critical("invalid code from table header at position 0x%x : %s" % (pos, RawDataHelper.str2hex(code)))
            else:
                # the number of remaining tables...
                (counter,) = struct.unpack('<I', buffer[:4])
                logger.warning('%i remaining tables at position 0x%x' % (counter, pos))
                pos += 4
                f.seek(pos, 0)
                buffer = f.read(80)
                continue
        f.seek(pos+tableSize+80)
        logger.info("header %s", unicode(('0x%x' % pos,name,itemSize,nbItem,tableSize)))
#        g = file(unicode(pos) + '.test', 'wb')
#        g.write(rawName)
#        g.close()
        h = headerClass()
        h.pos = pos
        h.name = name
        h.itemSize = itemSize
        h.nbItem = nbItem
        h.tableSize = tableSize
        yield h
        pos = f.tell()
        buffer = f.read(80)
    #f.close()

def itemSizeGenerator(heredisFile,tableName):
    try:
        h = heredisFile.tableHeaders[tableName]
    except KeyError:
        logger.warning("la table %s n'existe pas",tableName)
        return
    f = heredisFile.fdopen()
    pos = h.pos + 80 +  4
    endPos = h.pos + 80 + h.tableSize
    offset = 0
    while pos < endPos:
        f.seek(pos)
        b = f.read(4)
        o = struct.unpack('<I',b)[0]
        pos+=4
        size = o-offset
        if size < 0:
            logger.critical("Size is negative!\n new offset: %d\n current offset: %d\n size: %d\n current position: %d\n final position: %d", o, offset, size, pos, endPos)
        yield size
        offset = o
    #f.close()

def itemGenerator(heredisFile,tableName,unpackFct,objClass,itemSizeTableName=None):
    if not itemSizeTableName:
        itemSizeTableName = tableName+'-ItemSize'
    try:
        hItem = heredisFile.tableHeaders[tableName]
    except KeyError:
        logger.warning("la table %s n'existe pas",tableName)
        return
    f = heredisFile.fdopen()
    pos = hItem.pos
    hItem.endPos = hItem.pos + hItem.tableSize
    pos += 80
    for size in heredisFile.itemSizeGenerator(itemSizeTableName):
        f.seek(pos)
        if size <= 0:
            logger.critical("%s table des tailles incoherentes (given item size of %d, current position: %d (%x))",itemSizeTableName, size, pos, pos)
            if heredisFile.stopOnError:
                raise HeredisError,"table des tailles incoherentes"
            size = 400
        b = f.read(size)
        if pos + size > hItem.endPos:
            logger.warning("Item size is exceeding %s table size!", tableName)
        try:
            buf = Buffer.Buffer(b)
            yield unpackFct(buf, objClass())
        except Exception,e:
            logger.exception("Erreur dans la table %s",tableName)
            error = HeredisError("Erreur dans la table %s" % tableName)
            error.oldError = e
            raise e

        if tableName in heredisFile.tablesToRecover:
            if size != buf.index + heredisFile.tablesToRecover[tableName]:
                logger.warning("Trying to recover bad size! expected size: %d, readed size %d for table %s", size, buf.index, tableName)
                size = buf.index + heredisFile.tablesToRecover[tableName]
        pos += size
    #f.close()


def unpackIndividu(buffer,result):
    result.id = buffer.get('<I')[0]
    result.creationDate = buffer.get('<I')[0]
    result.modificationDate = buffer.get('<I')[0]
    result.fatherID = buffer.get('<I')[0]
    result.motherID = buffer.get('<I')[0]
    result.surnameID = buffer.get('<I')[0]
    result.unknown1 = buffer.get('<I')[0]
    result.name = buffer.getString()
    result.activity = buffer.getString()
    result.sex = buffer.getString()
    result.note = buffer.getString()
    result.numero = buffer.getString()
    result.userFields[0] = buffer.getString()
    result.userFields[1] = buffer.getString()
    result.userFields[2] = buffer.getString()
    result.userFields[3] = buffer.getString()
    result.userFields[4] = buffer.getString()
    result.userFields[5] = buffer.getString()
    result.userFields[6] = buffer.getString()
    result.userFields[7] = buffer.getString()
    result.userFields[8] = buffer.getString()
    result.userFields[9] = buffer.getString()
    result.userFields[10] = buffer.getString()
    result.unknown2 = buffer.get('<H')[0]
    result.sansDesc = buffer.get('<H')[0]
    result.signatureIndex = buffer.get('<B')[0]
    result.enfantIndex = buffer.get('<B')[0]
    result.marque = buffer.get('<B')[0]
    result.unknown3 = buffer.get('<B')[0]
    result.confidentiel = buffer.get('<B')[0]
    result.suffixe = buffer.getString()
    result.surnom = buffer.getString()
    result.titre = buffer.getString()
    return result

def unpackSurname(buffer,result):
    result.id = buffer.get('<I')[0]
    result.creationDate = buffer.get('<I')[0]
    result.modificationDate = buffer.get('<I')[0]
    result.mainSurnameID = buffer.get('<I')[0]
    result.name = buffer.getString()
    return result

def unpackUnion(buffer,result):
    result.id = buffer.get('<I')[0]
    result.creationDate = buffer.get('<I')[0]
    result.modificationDate = buffer.get('<I')[0]
    result.husbandID = buffer.get('<I')[0]
    result.wifeID = buffer.get('<I')[0]
    result.unknown1 = buffer.get('<I')[0]
    result.note = buffer.getString()
    return result

def unpackEvent(buffer,result):
    result.id = buffer.get('<I')[0]
    result.creationDate = buffer.get('<I')[0]
    result.modificationDate = buffer.get('<I')[0]
    result.itemID = buffer.get('<I')[0]
    result.type = buffer.get('<B')[0]
    result.placeID = buffer.get('<I')[0]
    result.unknown1 = buffer.get('<B')[0]
    result.calendar1 = buffer.get('<B')[0]
    result.calendar2 = buffer.get('<B')[0]
    result.modif1 = buffer.get('<B')[0]
    result.modif2 = buffer.get('<B')[0]
    result.day1 = buffer.get('<B')[0]
    result.day2 = buffer.get('<B')[0]
    result.month1 = buffer.get('<B')[0]
    result.month2 = buffer.get('<B')[0]
    result.modif3 = buffer.get('<B')[0]
    result.partYear1 = buffer.get('<B')[0]
    result.selectYear1 = buffer.get('<B')[0]
    result.partYear2 = buffer.get('<B')[0]
    result.selectYear2 = buffer.get('<B')[0]
    result.hour = buffer.get('<B')[0]
    result.minute = buffer.get('<B')[0]
    result.unknown2 = buffer.get('<16B')[0]
    result.note = buffer.getString()
    result.placeSubdivision = buffer.getString()
    result.name = buffer.getString()
    result.unknown3 = buffer.get('<H')[0]
    result.ageOnAct = buffer.getString()
    result.findTheSource = buffer.get('<B')[0]
    return result

def unpackPlace(buffer,result):
    result.id = buffer.get('<I')[0]
    result.creationDate = buffer.get('<I')[0]
    result.modificationDate = buffer.get('<I')[0]
    result.mainPlaceID = buffer.get('<I')[0]
    result.town = buffer.getString()
    result.code = buffer.getString()
    result.department = buffer.getString()
    result.region = buffer.getString()
    result.country = buffer.getString()
    return result

def unpackAddresse(buffer,result):
    result.id = buffer.get('<I')[0]
    result.creationDate = buffer.get('<I')[0]
    result.modificationDate = buffer.get('<I')[0]
    result.unionID = buffer.get('<I')[0]
    result.husbandID = buffer.get('<I')[0]
    result.wifeID = buffer.get('<I')[0]
    result.private = buffer.get('<H')[0]
    result.unknown1 = buffer.get('<B')[0]
    result.contact = buffer.getString()
    result.line1 = buffer.getString()
    result.line2 = buffer.getString()
    result.postalCode = buffer.getString()
    result.town = buffer.getString()
    result.country = buffer.getString()
    result.phone = buffer.getString()
    result.fax = buffer.getString()
    result.email = buffer.getString()
    result.region = buffer.getString()
    return result

def unpackSource(buffer,result):
    result.id = buffer.get('<I')[0]
    result.creationDate = buffer.get('<I')[0]
    result.modificationDate = buffer.get('<I')[0]
    result.unknown1 = buffer.get('<B')[0]
    result.origin = buffer.getString()
    result.document = buffer.getString()
    result.cote = buffer.getString()
    result.archivage = buffer.getString()
    result.type = buffer.get('<H')[0]
    result.unknown2 = buffer.get('<H')[0]
    result.note = buffer.getString()
    result.name = buffer.getString()
    return result

def unpackMedia(buffer,result):
    result.id = buffer.get('<I')[0]
    result.creationDate = buffer.get('<I')[0]
    result.modificationDate = buffer.get('<I')[0]
    result.directory = buffer.getString()
    result.fileName = buffer.getString()
    result.unknown1 = buffer.get('<B')[0]
    result.comment = buffer.getString()
    result.thumbnailLength = buffer.get('<I')[0]
    result.year1 = buffer.get('<B')[0]
    result.year2 = buffer.get('b')[0]
    result.unknown2 = buffer.get('<H')[0]
    result.unknown3 = buffer.get('<H')[0]
    result.thumbnail = buffer.remain()
    return result

def unpackLink(buffer,result):
    result.id = buffer.get('<I')[0]
    result.creationDate = buffer.get('<I')[0]
    result.modificationDate = buffer.get('<I')[0]
    result.fromItemID = buffer.get('<I')[0]
    result.toItemID = buffer.get('<I')[0]
    result.note = buffer.getString()
    result.unknown1 = buffer.get('<H')[0]
    result.typeIndex = buffer.get('<B')[0]
    return result

def unpackLinkDoc(buffer,result):
    result.id = buffer.get('<I')[0]
    result.creationDate = buffer.get('<I')[0]
    result.modificationDate = buffer.get('<I')[0]
    result.evtID = buffer.get('<I')[0]
    result.sourceID = buffer.get('<I')[0]
    result.note = buffer.getString()
    return result

def unpackLinkMedia(buffer,result):
    result.id = buffer.get('<I')[0]
    result.creationDate = buffer.get('<I')[0]
    result.modificationDate = buffer.get('<I')[0]
    result.ownerID = buffer.get('<I')[0]
    result.mediaID = buffer.get('<I')[0]
    result.mainMedia = buffer.get('<I')[0]
    return result
