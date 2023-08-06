import configparser
from os.path import expanduser
import os

class QplayConfig:
    """Commands for easy backtesting strategy
    """
    config_path = "{}/.quantplay".format(expanduser("~"))
    
    def __init__(self):
        pass
    
    @staticmethod
    def get_credentials():
        isExist = os.path.exists(QplayConfig.config_path)
        if not isExist:
            # Create a new directory because it does not exist 
            os.makedirs(QplayConfig.config_path)
        
        credentials = configparser.ConfigParser()
        credentials.read("{}/config".format(QplayConfig.config_path))
        
        return credentials