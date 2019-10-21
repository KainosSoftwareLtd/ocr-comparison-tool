from os import environ
from time import sleep
from requests import get, post

VISION_BASE_URL='https://northeurope.api.cognitive.microsoft.com/vision/v2.0/'
DOCUMENT_TEXT_URL='{0}{1}'.format(VISION_BASE_URL,'read/core/asyncBatchAnalyze')
IMAGE_TEXT_URL='{0}{1}'.format(VISION_BASE_URL,'ocr')

HEADER={'Ocp-Apim-Subscription-Key':environ.get('MICROSOFT_KEY'),
        'Content-Type':'application/octet-stream'}

def encode_image(file_path):
    return open(file_path,'rb').read()

def send_api_call(url,img,head=HEADER):
    return post(url,headers=head,data=img)

def get_document_obj(file_path):
    try:
        img_bytes=encode_image(file_path)
        async_url=send_api_call(DOCUMENT_TEXT_URL,img_bytes)

        #due to async nature, wait for response before returning
        reponse={}
        isFinished=False
        while(not(isFinished)):
            reponse=get(async_url.headers['Operation-Location'],headers=HEADER).json()
            isFinished=True if('recognitionResults' in reponse) or ('status' in reponse and reponse['status']=='Failed') else False
            sleep(1)
        return reponse
    except: return ''

def get_document_text(file_path):
    response=get_document_obj(file_path)
    try:
        text_uco=u' '.join(list(map(lambda x: x['text'],sum(map(lambda x: x['lines'],response['recognitionResults']),[])))).strip()
        return text_uco.encode('ascii','replace').decode('utf-8') 
    except: return ''        

def get_image_obj(file_path):
    img_bytes=encode_image(file_path)
    return send_api_call(IMAGE_TEXT_URL,img_bytes).json()

def get_image_text(file_path):
    response=get_image_obj(file_path)
    try:
        text_obj=list(map(lambda x: x['words'],sum(map(lambda x: x['lines'],response['regions']),[])))
        text_uco=u' '.join(list(map(lambda x: x['text'],sum(text_obj,[])))).strip()
        return text_uco.encode('ascii','replace').decode('utf-8')
    except: return ''

def ms_get_text(file_path,media='both'):
    if media=='both': return get_document_text(file_path),get_image_text(file_path)
    if media=='document': return get_document_text(file_path)
    if media=='image': return get_image_text(file_path)
    return '{} is an invalid media option'.format(media)