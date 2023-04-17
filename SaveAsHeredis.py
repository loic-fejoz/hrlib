import struct
import pack
import hrlib

def listSortedById(items):
    l = list(items)
    l.sort(lambda i1, i2: cmp(i1.id, i2.id))
    return l

def save(heredisFile, output):
    individus = listSortedById(heredisFile.individuGenerator())
    noms = listSortedById(heredisFile.surnameGenerator())
    unions = listSortedById(heredisFile.unionGenerator())
    events = listSortedById(heredisFile.eventGenerator())
    lieux = listSortedById(heredisFile.placeGenerator())
    adresses = listSortedById(heredisFile.addresseGenerator())
    sources = listSortedById(heredisFile.sourceGenerator())
    medias = listSortedById(heredisFile.mediaGenerator())
    links = listSortedById(heredisFile.linkGenerator())
    linkDocs = listSortedById(heredisFile.linkDocGenerator())
    linkMedias = listSortedById(heredisFile.linkMediaGenerator())

    output.write(pack.packFileHeader(heredisFile.getFileHeader()))
    dumpCkeckedPeoples(output)
    dumpTable(output, 'TH5TableIndividus', individus, pack.packIndividu)
    dumpIDTable(output, 'TH5TableIndividus', individus, pack.packIndividu)
    dumpTBPeople(output, individus)
    dumpTable(output, 'TH5TableDicoNoms', noms, pack.packSurname)
    dumpIDTable(output, 'TH5TableDicoNoms', noms, pack.packSurname)
    dumpPartNameTable(output)
    dumpSizeTable(output, 'TH5TableDicoNoms', noms, pack.packSurname)
    dumpIndividus(output, individus)
    dumpSizeTable(output, 'TH5TableIndividus', individus, pack.packIndividu)
    dumpTable(output, 'TH5TableEvenements', events, pack.packEvent)
    dumpIDTable(output, 'TH5TableEvenements', events, pack.packEvent)
    dumpTBEventIdx(output, events)
    dumpTable(output, 'TH5TableDicoLieux', lieux, pack.packPlace)
    if len(lieux)!=0:
        dumpIDTable(output, 'TH5TableDicoLieux', lieux, pack.packPlace)
        dumpTBPlaceIdxPlace(output, lieux)
        #TBPlace-IdxPlace-Match
        output.write(pack.packTableHeader('TBPlace-IdxPlace-Match', 8, 0, 0))
        dumpTBNomIdxCode(output, lieux)
        #TBPlace-IdxCode-Match
        output.write(pack.packTableHeader('TBPlace-IdxCode-Match', 8, 0, 0))
        
        dumpSizeTable(output, 'TH5TableDicoLieux', lieux, pack.packPlace)
    dumpSizeTable(output, 'TH5TableEvenements', events, pack.packEvent)
    dumpTable(output, 'TH5TableUnion', unions, pack.packUnion)
    dumpIDTable(output, 'TH5TableUnion', unions, pack.packUnion)
    dumpTBUnionIdxHusb(output, unions)
    dumpTBUnionIdxSpouse(output, unions)
    dumpSizeTable(output, 'TH5TableUnion', unions, pack.packUnion)
    dumpTable(output, 'TH5TableMedias', medias, pack.packMedia)
    dumpIDTable(output, 'TH5TableMedias', medias, pack.packMedia)
    if len(linkMedias)!=0:
        dumpTable(output, 'TBMedia-IdxOwner', linkMedias, pack.packLinkMedia,tableIDName='TH5LinkMedia-IDList')
        dumpIDTable(output, 'TBMedia-IdxOwner', linkMedias, pack.packLinkMedia,tableIDName='TH5LinkMedia-IDList')
        dumpSizeTable(output, 'TBMedia-IdxOwner', linkMedias, pack.packLinkMedia,tableIDName='TH5LinkMedia-IDList')
    dumpSizeTable(output, 'TH5TableMedias', medias, pack.packMedia)
    dumpTable(output, 'TBLINK', links, pack.packLink)
    dumpIDTable(output, 'TBLINK', links, pack.packLink)
    dumpTBLinkIdxVERS(output, links)
    dumpTBLinkIdxDE(output, links)
    dumpSizeTable(output, 'TBLINK', links, pack.packLink)
    dumpTable(output, 'TH5TableDicoAdresses', adresses, pack.packAddresse)
    dumpIDTable(output, 'TH5TableDicoAdresses', adresses, pack.packAddresse)
    dumpSizeTable(output, 'TH5TableDicoAdresses', adresses, pack.packAddresse)
    output.write(pack.packTableHeader('SOSATbl', 36, 0, 0))
    dumpTable(output, 'TH5Doc', sources, pack.packSource)
    dumpIDTable(output, 'TH5Doc', sources, pack.packSource)
    if len(linkDocs)!=0:
        dumpTable(output, 'TH5LinkDoc', linkDocs, pack.packLinkDoc)
        dumpIDTable(output, 'TH5LinkDoc', linkDocs, pack.packLinkDoc)
        dumpTBDocIdxDoc(output, linkDocs)
        dumpSizeTable(output, 'TH5LinkDoc', linkDocs, pack.packLinkDoc)
    dumpSizeTable(output, 'TH5Doc', sources, pack.packSource)
        
    
    
def dumpCkeckedPeoples(output):
    output.write(pack.packTableHeader('CkeckedPeoples', 4, 0, 0))

def dumpPartNameTable(output):
    partNames = ["d'", 'de ', 'van ', 'von ']
    ch = ''.join(map(lambda x: x+'\0', partNames))
    output.write(pack.packTableHeader('PartNameTbl', 4, len(partNames), len(ch)))
    output.write(ch)
    n = 1+len(partNames)
    output.write(pack.packTableHeader('PartNameTbl-ItemSize', 4, n, 4*n))
    delta = 0
    output.write(struct.pack('<I', delta))
    for p in partNames:
        delta += len(p) + 1
        output.write(struct.pack('<I', delta))

def dumpIndividus(output, individus):
    n = len(individus)
    # QuickList
    output.write(pack.packTableHeader('QuickList', 12, n, 12*n))
    for item in individus:
        output.write(struct.pack('<III', item.id, item.fatherID, item.motherID))
    # QuickList-Childs
    output.write(pack.packTableHeader('QuickList-Childs', 8, 0, 0))

def dumpTBPeople(output, individus):
    individus = individus[::]
    n = len(individus)
    # TBPeople-IdxAlpha
    output.write(pack.packTableHeader('TBPeople-IdxAlpha', 4, n, 4*n))
    individus.sort(lambda i1, i2: cmp(i1.surname.name, i2.surname.name) or cmp(i1.name, i2.name))
    for item in individus:
        output.write(struct.pack('<I',item.id))
    # TBPeople-IdxAlphaR
    output.write(pack.packTableHeader('TBPeople-IdxAlphaR', 4, n, 4*n))
    #individus.sort(lambda i1, i2: -cmp(i1.name, i2.name))
    # it seems that TBPeople-IdxAlphaR is identical to TBPeople-IdxAlpha !
    for item in individus:
        output.write(struct.pack('<I',item.id))

def dumpTBEventIdx(output, events):
    n = len(events)
    if n==0:
        return
    evts = events[::]
    output.write(pack.packTableHeader('TBEvent-Idx', 16, n, 16*n))
    evts.sort(lambda e1, e2: cmp(e1.itemID, e2.itemID))
    for evt in evts:
        output.write(struct.pack('<IIII', evt.itemID, 0, evt.type, evt.id))

def dumpTBUnionIdxHusb(output, unions):
    n = len(unions)
    if n==0:
        return
    output.write(pack.packTableHeader('TBUnion-IdxHusb', 8, n, 8*n))
    for union in unions:
        output.write(struct.pack('<II', union.husbandID, union.id))

def dumpTBUnionIdxSpouse(output, unions):
    n = len(unions)
    if n==0:
        return
    output.write(pack.packTableHeader('TBUnion-IdxSpouse', 8, n, 8*n))
    for union in unions:
        output.write(struct.pack('<II', union.wifeID, union.id))

def dumpTBDocIdxDoc(output, linkDocs):
    n = len(linkDocs)
    if n==0:
        return
    output.write(pack.packTableHeader('TBDoc-IdxDoc', 12, n, 12*n))
    for link in linkDocs:
        output.write(struct.pack('<III', link.evtID, link.sourceID, link.id))

def dumpTBLinkIdxDE(output, links):
    n = len(links)
    if n==0:
        return
    output.write(pack.packTableHeader('TBLink-IdxDE', 12, n, 12*n))
    for link in links:
        output.write(struct.pack('<III', link.toItemID, link.fromItemID, link.id))

def dumpTBLinkIdxVERS(output, links):
    n = len(links)
    if n==0:
        return
    output.write(pack.packTableHeader('TBLink-IdxVERS', 12, n, 12*n))
    for link in links:
        output.write(struct.pack('<III', link.fromItemID, link.toItemID, link.id))

def dumpTBPlaceIdxPlace(output, lieux):
    n = len(lieux)
    lieux = lieux[::]
    lieux.sort(lambda p1, p2: cmp(p1.town, p2.town))
    if n==0:
        return
    output.write(pack.packTableHeader('TBPlace-IdxPlace', 4, n, 4*n))
    for place in lieux:
        output.write(struct.pack('<I', place.id))

def dumpTBNomIdxCode(output, lieux):
    n = len(lieux)
    lieux = lieux[::]
    lieux.sort(lambda p1, p2: cmp(p1.code, p2.code))
    if n==0:
        return
    output.write(pack.packTableHeader('TBNom-IdxCode', 4, n, 4*n))
    for place in lieux:
        output.write(struct.pack('<I', place.id))

def dumpTable(output, tableName, items, packFunc, tableIDName=None, tableSizeName=None):
    if not tableIDName:
        tableIDName = tableName + '-IDList'
    if not tableSizeName:
        tableSizeName = tableName + '-ItemSize'
    offset = 0
    i = 0
    for item in items:
        i += 1
        item.buffer = packFunc(item)
        item.index = i
        item.offset = offset
        offset += len(item.buffer)
    # output item table
    output.write(pack.packTableHeader(tableName, 4, i, offset))
    if i == 0:
        return
    for item in items:
        output.write(item.buffer)

def dumpIDTable(output, tableName, items, packFunc, tableIDName=None, tableSizeName=None):
    if not tableIDName:
        tableIDName = tableName + '-IDList'
    i = len(items)
    if i == 0:
        return
    # output ID table
    output.write(pack.packTableHeader(tableIDName, 8, i, 8*i))
    for item in items:
        output.write(struct.pack('<II',item.id,item.index))

def dumpSizeTable(output, tableName, items, packFunc, tableIDName=None, tableSizeName=None):
    if not tableSizeName:
        tableSizeName = tableName + '-ItemSize'
    i = len(items)
    if i == 0:
        return
    # output size table
    output.write(pack.packTableHeader(tableSizeName, 4, i+1, 4*i + 4))
    for item in items:
        output.write(struct.pack('<I',item.offset))
    output.write(struct.pack('<I',item.offset+len(item.buffer)))

def test():
    #fileName = "fejoz"
    #fileName = "minimal"
    #fileName = 'simple'
    import LogService
    LogService.setLogStdOut('%(message)s')
    import sys
    fileName = sys.argv[1]
    hf = hrlib.open("%s.hr5" % fileName)
    output = file("%s_output.hr5" % fileName,'wb')
    save(hf,output)
    output.close()
    hf.close()
    hf = hrlib.open("%s_output.hr5" % fileName)
    hf.close()

if __name__=='__main__':
    test()
