# 2013.10.30 12:09:35 CET
from Components.Converter.Converter import Converter
from Components.Element import cached
from enigma import eTimer
from socket import socket, AF_INET, SOCK_STREAM
import os

class TestConnection(Converter, object):


    def __init__(self, type):
        Converter.__init__(self, type)
        self.Dominio  = 'Insert url or ip'		
        self.testOK = False
        self.testTime = 1.0
        self.testPause = 10
        self.testHost = '192.168.1.1'
        self.testPort = 80
        if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/iSkin/Connection/Config/ConnectionSave'):
               	type = open('/usr/lib/enigma2/python/Plugins/Extensions/iSkin/Connection/Config/ConnectionSave').read()	
        if len(type):
            p = type[:].find('://')
            if p != -1:
                type = type[(p + 3):]
            type = type[:].split(':')
            if len(type[0]) > 0:
                self.testHost = type[0]
            if len(type) > 1 and type[1].isdigit():
                self.testPort = int(type[1])
            if len(type) > 2 and type[2].isdigit():
                self.testPause = max(1, int(type[2]))
        self.testTimer = eTimer()
        self.testTimer.callback.append(self.test)
        self.testTimer.start(100, True)

    def test(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.settimeout(self.testTime)
        try:
            self.testOK = not bool(s.connect_ex((self.testHost, self.testPort)))
            self.Dominio  =   str(self.testHost )      	
        except:
            self.testOK = False
            self.Dominio  =   str(self.testHost)+' down'   			
        s.close()
        self.testTimer.start(self.testPause * 1000, True)



    @cached
    def getBoolean(self):
        return self.testOK
    boolean = property(getBoolean)

    @cached
    def getText(self):
	return str(self.Dominio)
    text = property(getText)