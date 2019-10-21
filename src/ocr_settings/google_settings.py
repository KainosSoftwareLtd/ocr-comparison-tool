from os import environ
from utils.file import log

def gc_init(ts):
    try: 
        environ['GOOGLE_APPLICATION_CREDENTIALS']='/path/to/your/secret/credential/.file.json'
        log(ts,True,'Credentials loaded for Google',mode='setup')
        return True
    except: return False