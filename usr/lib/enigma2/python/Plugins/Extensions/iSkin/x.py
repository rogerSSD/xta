import os
if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/iSkin/Connection/Config/ConnectionSave'):
               	type = open('/usr/lib/enigma2/python/Plugins/Extensions/iSkin/Connection/Config/ConnectionSave').read()	
if len(type):
            p = type[:].find('://')
            if p != -1:
                type = type[(p + 3):]
            type = type[:].split(':')
            if len(type[0]) > 0:
                print type[0]
            if len(type) > 1 and type[1].isdigit():
                print int(type[1])
            if len(type) > 2 and type[2].isdigit():
                print max(1, int(type[2]))