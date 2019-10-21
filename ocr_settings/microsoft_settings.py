from os import environ
from json import load
from utils.file import log

def ms_init(ts):
    try:
        MICROSOFT_ACCESS_CREDENTIALS='/path/to/your/secret/credential/.file.json'
        with open(MICROSOFT_ACCESS_CREDENTIALS) as f:
            environ['MICROSOFT_KEY']=load(f)['key']
        log(ts,True,'Credentials loaded for Microsoft',mode='setup')
        return True
    except: return False