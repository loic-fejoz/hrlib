# -*- coding: latin1 -*-
"""
The base class for all HeredisFile.
You should only call the open function.

GPL Copyright (C) 2004  Loïc Fejoz
"""
class FileProxy(object):
    def __init__(self, subject):
        self._subject = subject
        self._where = 0

    def read(self, n):
        self._subject.seek(self._where)
        s = self._subject.read(n)
        self._where = self._subject.tell()
        return s

    def tell(self):
        return self._where

    def seek(self, pos, whence=0):
        self._subject.seek(pos, whence)
        self._where = self._subject.tell()

    def close(self):
        pass
        
