# -*- coding: latin1 -*-
import Item
import sets

class Event(Item.Item):
    gedcom_calendriers = {0x4a:u'@#DJULIAN@',
                          0x00:u'@#DGREGORIAN@',
                          0x48:u'@#DHEBREW@',
                          0x52:u'@#FRENCH R@'}

    modifList = [u'',
                 u'après',
                 u'avant',
                 u'entre',
                 u'vers',
                 u'calculé',
                 u'estimé',
                 u'et']
    
    evenementTypes = {4:u'naissance',
                     8:u'baptême',
                     12:u'décès',
                     16:u'diplôme',
                     6:u'inhumation',
                     24:u'acquisition',
                     34:u'adoption',
                     1:u'autre Baptême',
                     9:u'bapteme adulte',
                     2:u'bar Mitzvah',
                     3:u'bas Mitzvah',
                     5:u'bénédiction',
                     10:u'confirmation',
                     35:u'crémation',
                     25:u'décoration',
                     13:u'emigration',
                     26:u'en vie',
                     20:u'homologation de testament',
                     17:u'immigration',
                     18:u'naturalisation',
                     19:u'ordination',
                     32:u'première communion',
                     23:u'profession',
                     7:u'recensement',
                     30:u'résidence',
                     21:u'retraite',
                     27:u'service militaire',
                     31:u'testament',
                     33:u'titre',
                     28:u"vente d'un bien",
                     29:u'voyage',
                     0:u'baptême LDS',
                     11:u'confirmation LDS',
                     14:u'dotation LDS',
                     22:u'liens parental LDS',
                     61:u'union',
                     54:u'divorce',
                     68:u'mariage religieux',
                     55:u'demande de divorce',
                     66:u'adoption',
                     67:u'anulation du mariage',
                     58:u'bans',
                     59:u'contrat de mariage',
                     60:u'certification de publication des bans',
                     64:u'domicile',
                     57:u'évènement',
                     15:u'évènement',
                     56:u'fiançailles',
                     65:u'séparation',
                     63:u'lien conjugal LDS',
                      53:u'?'}

    id = None
    creationDate = 0
    modificationDate = 0
    itemID = None
    type = None
    placeID = None
    calendar1 = 0
    calendar2 = 0
    modif1 = None
    modif2 = None
    day1 = None
    day2 = None
    month1 = None
    month2 = None
    modif3 = None
    partYear1 = None
    selectYear1 = None
    partYear2 = None
    selectYear2 = None
    hour = None
    minute = None
    note = u''
    placeSubdivision = None
    name = u''
    ageOnAct = None
    findTheSource = False
    
    def __init__(self):
        self.links = sets.Set()
        self.reverseLinks = sets.Set()
        self.linkMedias = sets.Set()
        self.linkDocs = sets.Set()
	
    def getYear1(self):
        return 256 * self.selectYear1 + self.partYear1
	
    def getYear2(self):
        return 256 * self.selectYear2 + self.partYear2
            
    def setYear1(self,year):
        self.selectYear1 = int(year/256)
        self.partYear1 = year - self.selectYear1 * 256

    def setYear2(self,year):
        self.selectYear2 = int(year/256)
        self.partYear2 = year - self.selectYear2 * 256

    year1 = property(getYear1,setYear1,doc="year of the first date")
    year2 = property(getYear2,setYear2,doc="year of the second date")

    def getTypeName(self):
        return self.evenementTypes.get(self.type,str(self.type))

    typeName = property(getTypeName)

    def getSimpleDate(self):
        def simpleDate(cal,day,month,year,modif):
            return u"%s %s %d/%d/%d" % (self.modifList[modif],self.gedcom_calendriers[cal],day,month,year)
        if self.modif1 == 3:
            result = "%s %s" % (simpleDate(self.calendar1,self.day1,self.month1,self.year1,self.modif1),simpleDate(self.calendar2,self.day2,self.month2,self.year2,self.modif2))
        else:
            result = simpleDate(self.calendar1,self.day1,self.month1,self.year1,self.modif1)
        return result.strip()
