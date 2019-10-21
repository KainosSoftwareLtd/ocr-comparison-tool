from os import environ
from utils.file import log

def aws_init(ts):    
    try:
        environ['AWS_SHARED_CREDENTIALS_FILE']='/path/to/your/secret/credential/.file.txt'
        environ['AWS_CONFIG_FILE']='/path/to/your/secret/config/.file.txt'
        log(ts,True,'Credentials loaded for Amazon',mode='setup')
        return True
    except: return False