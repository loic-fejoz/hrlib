import struct

def str2hex(ch):
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

class Buffer:
    """This is buffer where you can unpack data more easily"""
    def __init__(self,buffer='',charCode='latin_1'):
        self.buffer = buffer
        self.index = 0
        self.charCode = charCode

    def get(self,format):
        """like struct.unpack"""
        size = struct.calcsize(format)
        i = self.index
        result = struct.unpack(format,self.buffer[i:i+size])
        self.index = i + size
        return result

    def set(self,format,value):
        """ append the result of struct.pack """
        self.buffer = self.buffer + struct.pack(format,value)

    def getString(self,size = None,charCode=None):
        """return a string that finish by a nul character"""
        b = self.buffer
        i = b.find('\x00',self.index)
        result = b[self.index:i]
        if size:
            self.index += size
        else:
            self.index = i + 1
        if charCode:
            return unicode(result.decode,charCode)
        elif self.charCode:
            return unicode(result,self.charCode)
        else:
            return unicode(result)

    def setString(self,str):
        """ append str to this buffer """
        if type(str) == type(u''):
            self.buffer += str.encode('latin_1') + '\0'
        else:
            self.buffer += str + '\0'

    def skip(self,b=None,format=None):
        """ skip b bytes or size of format"""
        if format:
            b = struct.calcsize(format)
        self.index += b

    def addDummy(self,b=0,format=None):
        """ append b bytes or size of format null bytes"""
        if format:
            b = struct.calcsize(format)
        self.buffer += b * '\0'

    def addRaw(self,raw):
        self.buffer += raw

    def remain(self):
        return self.buffer[self.index:]

    def dump(self):
        print self.buffer
        print str2hex(self.buffer)

    def __len__(self):
        return len(self.buffer)

    def lenRemain(self):
        return len(self.buffer[self.index:])
