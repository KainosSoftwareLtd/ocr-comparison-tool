from os import environ
from .amazon_settings import aws_init
from .google_settings import gc_init
from .microsoft_settings import ms_init
from utils.file import log
from utils.misc import get_timestamp

def init():
    ts=get_timestamp()
    try:
        aws_init(ts)
        gc_init(ts)
        ms_init(ts)
        log(ts,True,'All OCR services\' settings loaded',mode='setup')
    except: log(ts,False,'There was an issue loading all of the OCR services\' settings',mode='setup')
    try:
        environ['CHARACTER_SCRIPT_PATH']='/path/to/script/CharacTER.py'
        log(ts,True,'CharacTER\'s path set',mode='setup')
    except: log(ts,False,'There was an issue setting CharacTER\'s script path',mode='setup')

init()