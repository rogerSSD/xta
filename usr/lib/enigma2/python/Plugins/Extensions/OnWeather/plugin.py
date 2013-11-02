from Plugins.Plugin import PluginDescriptor
from Components.config import config

try:
    from Plugins.Extensions.iSkin.Weather.Weather import *
    jWeather = True		
except:
    jWeather = False	
	
def Main(session, **kwargs):
        session.open(MeteoMain)       
   		
def setup(menuid):
       if jWeather:
		if config.skin.primary_skin.value == 'xta/skin.xml': 
			if menuid == 'mainmenu':
				return [(_('YWeather'), Main,'YWeather',46)]
			else:			
				return []
		else: 
			return []		
       else:
	   return []	
	   
def Plugins(**kwargs):
        return PluginDescriptor(name = 'YWeather', description = 'CityWeather Setup', where = PluginDescriptor.WHERE_MENU, fnc=setup)		