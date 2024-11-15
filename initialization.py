import constants
from jproperties import Properties
import googledrive
import postgres

def init():
    print("initialization started...")
    constants.configs = Properties()
    constants.CREDS['drive'] = googledrive.init()
    postgres.init()
