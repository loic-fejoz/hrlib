#!/usr/bin/python
# -*- coding: latin-1 -*-
import sys
import logging
from optparse import OptionParser
parser = OptionParser(usage="%prog [options] fichier_heredis\nSee <http://hrlib.sourceforge.net/>")
parser.add_option("-f", "--file", dest="logging_file",
                  help="write logging to FILE", metavar="FILE")
parser.add_option("-i", "--individu",
                  action="store_true", dest="individu", default=False,
                  help="print all individus full names")
parser.add_option("-t", "--tables",
                  action="store_true", dest="tables", default=False,
                  help="print all tables name")
parser.add_option("-a", "--address",
                  action="store_true", dest="address", default=False,
                  help="print all addresses")
parser.add_option("-k", "--keepgoing",
                  action="store_true", dest="keepgoing", default=False,
                  help="Continue malgre des erreurs")
parser.add_option("-v", action="count", dest="verbosity", default=0, help="From 1 to 4 to increase verbosity (critical, error, warning, info, debug)")
(options, args) = parser.parse_args()
if len(args) ==1 and args[0] == 'show':
    print __doc__
    sys.exit(0)
if len(args) != 1:
    print "nombre  d'arguments  incorrect"
    parser.print_help()
    sys.exit(1)

# Set logger
logger = logging.getLogger()
# Use given file as error log or use stderr
if options.logging_file:
    hdlr = logging.FileHandler(options.logging_file)
else:
    hdlr = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
#set Level from the given verbosity option
LEVELS = {0: logging.CRITICAL,
          1: logging.ERROR,
          2: logging.WARNING,
          3: logging.INFO,
          4: logging.DEBUG}
logger.setLevel(LEVELS.get(options.verbosity, logging.NOTSET))

import HeredisFileMemory

print 'File:', args[0]
h = HeredisFileMemory.open(args[0], stopOnError = not options.keepgoing, tablesToRecover={'TH5TableIndividus': 2})
header = h.fileHeader
if header.software:
    print 'Software:', header.software
if header.software_version:
    print 'Software version:', header.software_version
print 'Version:', header.version, header.versionComplete
if header.name:
    print 'Name:', header.name
if header.comment:
    print 'Comment:', header.comment

if options.tables:
    print '-' * 80
    for table in h.tableHeaderGenerator():
        print table.name

if options.individu:
    print '-' * 80
    for i in h['individus'].itervalues():
        print i.fullName

if options.address:
    print '-' * 80
    for a in h.addressGenerator():
        if a.email:
            print a.email
