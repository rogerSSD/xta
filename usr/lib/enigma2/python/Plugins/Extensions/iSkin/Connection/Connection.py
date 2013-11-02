# -*- coding: UTF-8 -*-
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Components.Label import Label
from Components.config import config, ConfigIP, NoSave, ConfigText, ConfigSelection, getConfigListEntry, ConfigInteger,KEY_LEFT, KEY_RIGHT
from Components.ConfigList import ConfigListScreen,ConfigList
from Components.PluginComponent import plugins
from Components.ActionMap import ActionMap
from Plugins.Plugin import PluginDescriptor
from enigma import eTimer
from Screens.MessageBox import MessageBox
from Components.Harddisk import harddiskmanager
import os,re
DirConfigConnection = "/usr/lib/enigma2/python/Plugins/Extensions/iSkin/Connection/Config/ConnectionSave"
DirConfig = "/usr/lib/enigma2/python/Plugins/Extensions/iSkin/Connection/Config/ConfigSave"
class ConfigConnection(Screen, ConfigListScreen):

        def __init__(self, session):
            path = "/usr/lib/enigma2/python/Plugins/Extensions/iSkin/Skin/Connection.xml" 
            with open(path, "r") as f:
                    self.skin = f.read()
                    f.close() 	       					
            Screen.__init__(self, session)      
            self.ConfigConnection = []			
            self["config"] = ConfigList(self.ConfigConnection)	     
            self["Key_Red"] = Label(_("Exit"))
            self["Key_Green"] = Label("Save")		
            ConfigListScreen.__init__(self, self.ConfigConnection, session = self.session)  				
            self["myActionMap"]  = ActionMap(["SetupActions","ColorActions","DirectionActions"], 
            {		
                "left" : self.left,		
                "right" : self.right,						
                "ok" : self.OkKeyBoard,			
                "green": self.KeySave,							
                "cancel": self.KeyCancel
            }, -1)
            self.Config()		
            self.LoadConfig()	
            self.onLayoutFinish.append(self.MyConfigList)
                                                                                                                                 
        def getCurrentConfigPath(self):
            return self["config"].getCurrent()[2]
                                           
        def OkKeyBoard(self):
            if self.getCurrentConfigPath() == 'Url':
                self.session.openWithCallback(self.KeyBoardCallbackUrl, VirtualKeyBoard, title = (_("Insert Url")), text = self.SelectUrl.value)
            elif self.getCurrentConfigPath() == 'Ip':
                self.session.openWithCallback(self.KeyBoardCallbackIp, VirtualKeyBoard, title = (_("Insert Ip")), text = self.SelectIp.value)
                                
        def KeyBoardCallbackUrl(self, callback = None, entry = None):
            if callback is not None and len(callback):
                self.SelectUrl.setValue(str(callback))
				
        def KeyBoardCallbackIp(self, callback = None, entry = None):
            if callback is not None and len(callback):
                self.SelectIp.setValue(str(callback))

        def left(self):                                                 
            self["config"].handleKey(KEY_LEFT)
            self.MyConfigList()	
															 
	def right(self):                        
            self["config"].handleKey(KEY_RIGHT)
            self.MyConfigList()	
				
        def MyConfigList(self):		
            self.ConfigConnectionList = []			
            self.ConfigConnectionList.append(getConfigListEntry(_('Select type Connection Insert :'), self.SelectConf,'UrlIp'))
            if self.SelectConf.value == '1':	
                   self.ConfigConnectionList.append(getConfigListEntry(_('Insert Url :'), self.SelectUrl,'Url'))
            else:	
                   self.ConfigConnectionList.append(getConfigListEntry(_('Insert Ip :'), self.SelectIp,'Ip'))					   				   
            self.ConfigConnectionList.append(getConfigListEntry(_('Transaction Port :'), self.TransPort,'Port'))				
            self.ConfigConnectionList.append(getConfigListEntry(_('Timer Refresh :'), self.Timer,'Timer'))
            self["config"].l.setList(self.ConfigConnectionList)

        def Config(self):		
            self.SelectConf = NoSave(ConfigSelection([("1", _("Url")), ("0", _("Ip"))], default = "1"))			
	    self.SelectUrl = NoSave(ConfigText(default = "www.google.com", fixed_size = False))
            self.SelectIp = NoSave(ConfigIP(default = [192,168,1,1]) or [0,0,0,0])	
            self.TransPort = NoSave(ConfigInteger(default = 80, limits = (00000,65535)))
            self.Timer = NoSave(ConfigInteger(default = 120, limits = (1,999)))				
		
        def LoadConfig(self):
            try:
               try:
                  xf = open(DirConfig, "r")
                  f = xf.readlines()				
                  xf.close()		
               except Exception, e:
                  return                  
               for line in f:			   
                  LoadConf = line.strip()						  
                  if LoadConf.find('AddressIp') != -1 :	
                      Addres =str(LoadConf.split('AddressIp')[1].strip())
                      Ip0= int(Addres.split('.')[0])
                      Ip1= int(Addres.split('.')[1])
                      Ip2= int(Addres.split('.')[2])
                      Ip3= int(Addres.split('.')[3])				  
                      self.SelectIp = NoSave(ConfigIP(default = [Ip0,Ip1,Ip2,Ip3]))	
                  elif LoadConf.find('SelectUrl') != -1 :
                      self.SelectUrl.setValue(int(str(LoadConf.split('SelectUrl')[1].strip())))						  
                  elif LoadConf.find('Port') != -1 :
                      self.TransPort.setValue(int(str(LoadConf.split('Port')[1].strip())))	
                  elif LoadConf.find('Refresh') != -1 :
                      self.Timer.setValue(int(str(LoadConf.split('Refresh')[1].strip())))	
                  elif LoadConf.find('ConnectionType') != -1 :
                      self.SelectConf.setValue(str(LoadConf.split('ConnectionType')[1].strip()))						
            except:
                pass 
			
        def KeySave(self):
            Ip0 = Ip1 = Ip2 = Ip3 = '0'
            a=open(DirConfig, "w") 		
            a.write("ConnectionType %s\n" % (self.SelectConf.value))			
            a.write("AddressUrl %s\n" % (self.SelectUrl.value))			
            try:			
                         Ip0 = str(self.SelectIp.value[0])	
                         Ip1 = str(self.SelectIp.value[1])		
                         Ip2 = str(self.SelectIp.value[2])		
                         Ip3 = str(self.SelectIp.value[3])
            except:
                         pass				 
            a.write("AddressIp %s\n" % (Ip0+'.'+Ip1+'.'+Ip2+'.'+Ip3))	
            a.write("Port %s\n" % (self.TransPort.value))		
            a.write("Refresh %s\n" % (self.Timer.value))					
            a.close()	 			
            self.ConnectionSave()
            self.KeyCancel()
			
        def ConnectionSave(self):
            Ip0 = Ip1 = Ip2 = Ip3 = '0'
            a=open(DirConfigConnection, "w") 		
            if self.SelectConf.value == '1':		
                     Link = self.SelectUrl.value
            else:					 
                 try:			
                         Ip0 = str(self.SelectIp.value[0])	
                         Ip1 = str(self.SelectIp.value[1])		
                         Ip2 = str(self.SelectIp.value[2])		
                         Ip3 = str(self.SelectIp.value[3])
                 except:
                         pass				 
                 Link =(Ip0+'.'+Ip1+'.'+Ip2+'.'+Ip3)
            Port = self.TransPort.value
            Timer = self.Timer.value					
            a.write(str(Link)+':'+str(Port)+':'+str(Timer))					
            a.close()	
			
        def KeyCancel(self):
            self.close()	   	

