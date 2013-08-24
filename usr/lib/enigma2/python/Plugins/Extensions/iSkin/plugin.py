# SkinSelect by m43c0 23-08-2013
from Components.Label import Label
from Components.ConfigList import ConfigListScreen,ConfigList
from Components.ActionMap import ActionMap,NumberActionMap
from Components.config import KEY_LEFT, KEY_RIGHT,config,  getConfigListEntry , ConfigSelection, ConfigSubsection
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmap, MultiContentEntryPixmapAlphaTest
from enigma import  loadPic, gFont, eTimer, loadPNG, getDesktop, eListboxPythonMultiContent, RT_HALIGN_LEFT, eListbox, quitMainloop
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from time import *
import  re, os,sys, xml.etree.cElementTree,glob

import gettext
def _(txt):
	t = gettext.dgettext("iSkin", txt)
	if t == txt:
		print "[iSkin] fallback to default translation for", txt
		t = gettext.gettext(txt)
	return t
	
class ConfigSkin(Screen, ConfigListScreen):

        def __init__(self, session,selection):
                self.session = session
                self.selection = selection                               
                path = "/usr/lib/enigma2/python/Plugins/Extensions/iSkin/Skin/Setup.xml" 
                with open(path, "r") as f:
                    self.skin = f.read()
                    f.close() 	                                                
                mdom = xml.etree.cElementTree.parse(path)
                for x in mdom.getroot():
                    if x.tag == "widget" and x.get("name") == 'cover':
                        Size = x.get('size').split(',')
                        self.SizeY = int(Size[0]) 
                        self.SizeX = int(Size[1])                                                
                Screen.__init__(self, session)      
                self["Key_Red"] = Label(_("Exit"))		
                self["Key_Green"] = Label(_("Ok"))				
                self['title'] = Label(_("Select Skin ")+selection )                                    
                self['cover'] = Pixmap()	                                
                self.isMoving = False	                                
                self.Loop = eTimer()
                self.Loop.stop()		
                self.Loop.callback.append(self.Cover)   				
                self.LoopQuit = eTimer()
                self.LoopQuit.stop()		
                self.LoopQuit.callback.append(self.Riavvio)  				                                
                self.configlist = []	       
                self["config"] = ConfigList(self.configlist)	
                self.MyConfigList()        				
                ConfigListScreen.__init__(self, self.configlist, session = self.session)               
                self["setupActions"] = ActionMap(["SkinActionSetup"],
                                {
                                "down": self.down,
                                "up": self.up,
                                "ok": self.keyOK,
                                "green": self.keyOK,								
                                "left" : self.KeyLeft,
                                "right": self.KeyRight,
                                "red": self.close,								
                                "cancel": self.close
                                }, -1)   
                                
        def MyConfigList(self):	
                mdom = xml.etree.cElementTree.parse(os.path.dirname(sys.modules[__name__].__file__) + "/Config/SkinSetup.xml")
                config.Skin = ConfigSubsection()			 
                self.configlist = []					
                for x in mdom.getroot():
                    if x.tag == "ruleset" and x.get("name") == self.selection:
                        root = x								
                for x in root:
                    if x.tag == "set":  			
                        nome = x.get("name")						
                        MyList = self.listaselect(x)	
                        list =[]
                        for x in MyList:
                            list.append((x[0]+'****'+x[2],x[1]))			 
                        config.Skin.i = ConfigSelection(choices = list)
                        self.configlist.append(getConfigListEntry(nome,config.Skin.i,nome))	
                self.configlist.sort(key=lambda t : tuple(t[0][0].lower()))						
                self["config"].list = self.configlist		                               				
                self["config"].l.setList(self.configlist)
                self.Loop.start(100,True)
                
        def Cover(self):
                try:
                    self.Loop.stop()
                except:
                    pass	
                try:						
                    png = loadPic(str(self.getCurrentConfigPath()),self.SizeY,self.SizeX, 0, 0, 0, 1)			
                    self['cover'].instance.setPixmap(png)	
                    self['cover'].show() 
                except:
                    pass	
                                         
        def getCurrentConfigPath(self):		
                self.File = []              				
                for x in self["config"].list:		
                    tipo = str(x[1].value)				
                    if  self["config"].getCurrent()[2] == x[0]:	 
                        self.File.append(str(tipo))						   
                    else:
                        self.File.append(str(tipo))							   
                tipo = ''						   
                for x in self["config"].list:		
                    tipo = str(x[1].value)
                    if  self["config"].getCurrent()[2] == x[0]:	      			                             
                        tipo = tipo.replace('xml','png').split('****')[1]							  							  
                        break				  
                return tipo					
                                
        def KeyLeft(self):  
                try:
                   self["config"].handleKey(KEY_LEFT)				
                   self.Loop.start(100,True)
                except: 
                   pass
                                   
        def KeyRight(self):   		
                try:
                   self["config"].handleKey(KEY_RIGHT)				
                   self.Loop.start(100,True)
                except: 
                   pass
                                   
        def up(self):                 		
                if not self.isMoving:                                            
                    self["config"].instance.moveSelection(self["config"].instance.moveUp)   	
                    self.Loop.start(100,True)       
                          
        def down(self):    	
                if not self.isMoving:
                    self["config"].instance.moveSelection(self["config"].instance.moveDown) 						
                    self.Loop.start(100,True)                                           
                                                              
        def keyOK(self):
                self.session.openWithCallback(self.iKeyOk, MessageBox, _("The change requires a restart of E2, you want to proceed ?"), MessageBox.TYPE_YESNO, default = False)
                                
        def iKeyOk(self, answer):						
                if answer:  		
                    for x in self.File:
                        tipo = x.split('****')
                        os.system('cp '+tipo[1]+' '+tipo[0])
                    self.session.open(MessageBox, _("Restart E2 running!"), MessageBox.TYPE_INFO)
                    self.LoopQuit.start(3000,True)			

        def Riavvio(self):							
                quitMainloop(3)				   
                                                                    
        def listaselect(self,root):
                Directory=Tipo=Path=''	
                list =[]		
                for x in root:
                    if x.tag == "rule":  
                        if x.get("type") == 'skin':		  	
                            Directory =  x.get("Path")			
                        elif x.get("type") == 'panel':                
                            Tipo = x.get("Nome")	  
                            Path = x.get("Path")
                            if not os.path.exists(Path): 	
                                Tipo = _('Not Path ')+Tipo								
                    if  Directory and Tipo and Path: 		
                        list.append(( Directory,Tipo,Path))
                return list
                                
class iMenuList(MenuList):

        def __init__(self, list):
                MenuList.__init__(self, list, True, eListboxPythonMultiContent)
                self.l.setFont(0, gFont("Regular", 20))
                self.l.setItemHeight(44)

class MenuStart(Screen):

        def __init__(self, session):
                self.session = session
                path = "/usr/lib/enigma2/python/Plugins/Extensions/iSkin/Skin/Main.xml"                     
                with open(path, "r") as f:
                    self.skin = f.read()
                    f.close()	                                                      
                mdom = xml.etree.cElementTree.parse(path)
                for x in mdom.getroot():
                    if x.tag == "widget" and x.get("name") == 'cover':
                        Size = x.get('size').split(',')
                        self.SizeY = int(Size[0]) 
                        self.SizeX = int(Size[1])                                               
                Screen.__init__(self, session)                                        
                self["Key_Red"] = Label(_("Exit"))		
                self["Key_Green"] = Label("")
                self["Key_Yellow"] = Label("")		
                self["Key_Blu"] = Label("")	                                
                self['SkinSelect'] = iMenuList([])                                
                self.isMoving = False	
                self['cover'] = Pixmap()				
                self.Loop = eTimer()
                self.Loop.stop()		
                self.Loop.callback.append(self.Cover)                                   
                self["setupActions"] = ActionMap(["SkinActionSetup"],
                                { 
                                "ok": self.keyOK,
                                "up" : self.up,
                                "down":self.down,
                                "cancel": self.close
                                }, -1)				
                self.onLayoutFinish.append(self.layoutFinished)
                                
        def Cover(self):
                try:
                    self.Loop.stop()
                except:
                    pass	
                try:						 
                    png = loadPic(str(self.getCurrentConfigPath()),self.SizeY,self.SizeX, 0, 0, 0, 1)			
                    self['cover'].instance.setPixmap(png)	
                    self['cover'].show() 
                except:
                    pass
                                
        def getCurrentConfigPath(self):				  
                return self['SkinSelect'].getCurrent()[0][1]					
                                
        def up(self):                           
                if not self.isMoving:                                            
                    self["SkinSelect"].instance.moveSelection(self["SkinSelect"].instance.moveUp)                                                                       
                    self.Loop.start(100,True)       
                          
        def down(self):                         
                if not self.isMoving:
                    self["SkinSelect"].instance.moveSelection(self["SkinSelect"].instance.moveDown) 
                    self.Loop.start(100,True)       
                                                
        def layoutFinished(self):	
                mdom = xml.etree.cElementTree.parse(os.path.dirname(sys.modules[__name__].__file__) + "/Config/SkinSetup.xml")
                self.SkinSelect = []		
                for x in mdom.getroot():
                    if x.tag == "ruleset":		
                        self.SkinSelect.append(self.ListEntry(x.get("name"),x.get("Icon")))		               
                self.SkinSelect.sort(key=lambda t : tuple(t[0][0].lower()))
                self["SkinSelect"].setList(self.SkinSelect)				
                self.Loop.start(100,True)   
                                
        def ListEntry(self, name, jpg):
                res = [(name, jpg)]		
                icon = "/usr/lib/enigma2/python/Plugins/Extensions/iSkin/Skin/no_icon.png"
                res.append(MultiContentEntryPixmapAlphaTest(pos=(0, 1), size=(75, 40), png=loadPNG(icon)))	
                res.append(MultiContentEntryText(pos=(70, 4), size=(600, 30), font=0, text=name, flags=RT_HALIGN_LEFT))
                return res
                                
        def keyOK(self): 			
                exist = self['SkinSelect'].getCurrent()
                if exist == None:
                    return
                selection = self['SkinSelect'].getCurrent()[0][0]	
                self.session.open(ConfigSkin,selection) 
                
def Main(session, **kwargs):
        session.open(MenuStart)       
		
    		
def setup(menuid):
    #if config.skin.primary_skin.value == 'xta/skin.xml': 
        if menuid == 'setup':
            return [(_('XtrendSkins') + " " + _('Setup'), Main,'MenuStart',45)]
        else:			
            return []
    #else:
        #return []		

def Plugins(**kwargs):
        return PluginDescriptor(name = 'Skin Selection', description = 'For changing skin of mmark', where = PluginDescriptor.WHERE_MENU, fnc=setup)	
		
"""
def Plugins(**kwargs):
        return PluginDescriptor(name = 'Skin Selection', description = 'For changing skin of mmark', icon = 'SkinSelection.png', where = [PluginDescriptor.WHERE_EXTENSIONSMENU,PluginDescriptor.WHERE_PLUGINMENU], fnc = Main)
"""
                                            
