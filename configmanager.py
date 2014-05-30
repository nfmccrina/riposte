import configobj
import os
import os.path

class ConfigManager:
    def __init__(self):
        self.config = None

    def load_settings(self, argfile=None):
        if argfile:
            if os.path.exists(argfile):
                return self.process_file(argfile)         
            elif os.path.exists(os.environ['HOME'] + '/.config/riposte/riposte'):
                return self.process_file(os.environ['HOME'] + '/.config/riposte/riposte')
            else:
                return {}
        elif os.path.exists(os.environ['HOME'] + '/.config/riposte/riposte'):
            return self.process_file(os.environ['HOME'] + '/.config/riposte/riposte')
        else:
            return {}

    def process_file(self, configfile):
        return configobj.ConfigObj(configfile)            
        
