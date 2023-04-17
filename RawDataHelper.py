"""
Some usefull functions use in unpack to decode raw data
"""
import struct
import types

def getFileSize(f):
    """return the size of a file"""
    #remmber current position
    pos = f.tell()
    f.seek(0,2)
    size = f.tell()
    #go to previous position
    f.seek(pos)
    return size

def str2hex(ch):
    """return a string that represent the former string in hexadecimal"""
    result = ""
    for i in range(0,len(ch)):
        if i % 2 == 0 and i!= 0:
            result = result + " "
        c = ord(ch[i])
        h = hex(c)[2:]
        if len(h) == 1:
            h = "0" + h
        result = result + h
    return result

def int2bin(i):
    """ return a string representing the argument in binary """
    if i == 0:
        return "0"
    result = ""
    remainder = i
    while (remainder <> 0):
        j = remainder % 2;
        result = str(j) + result
        remainder = remainder / 2
    return result


def get(format,buffer,index):
    """get the data describe by format from the index position in the buffer"""
    size = struct.calcsize(format)
    result = struct.unpack(format,buffer[index:index+size])
    return result

def set(format,buffer,index,value):
    size = struct.calcsize(format)
    val = struct.pack(format,value)
    return buffer[:index] + val + buffer[index+size:]

def cString2String(obj,charCode='cp1252'):
    """return a unicode string from a string finished by a zero"""
    if type(obj) in [types.TupleType,type((1,))]:
        return map(lambda x:cString2String(x),obj)
    elif type(obj)  in [types.StringTypes,type('')]:
        i = obj.find('\x00')
        if i != -1:
            return unicode(obj[:i],charCode)
        else:
            return unicode(obj,charCode)
    else:
        return obj
