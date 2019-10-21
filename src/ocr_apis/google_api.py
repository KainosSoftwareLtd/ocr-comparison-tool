from google.cloud import vision
from os import environ
from json import loads
from google.protobuf.json_format import MessageToJson

def encode_image(file_path):
    with open(file_path,'rb') as f:
        return vision.types.Image(content=f.read())

def get_document_obj(file_path):
    client=vision.ImageAnnotatorClient()    
    img_bytes=encode_image(file_path)
    return loads(MessageToJson(client.document_text_detection(image=img_bytes)))

def get_document_text(file_path):
    response=get_document_obj(file_path)
    try:
        text_uco=u' '.join(response['textAnnotations'][0]['description'].split('\n')).strip()
        return text_uco.encode('ascii','replace').decode('utf-8')
    except: return ''

def get_image_obj(file_path):
    client=vision.ImageAnnotatorClient()
    img_bytes=encode_image(file_path)
    return loads(MessageToJson(client.text_detection(image=img_bytes)))

def get_image_text(file_path):
    response=get_image_obj(file_path)
    try:
        text_uco=u' '.join(response['textAnnotations'][0]['description'].split('\n')).strip()
        return text_uco.encode('ascii','replace').decode('utf-8')
    except: return ''

def gc_get_text(file_path,media='both'):
    if media=='both': return get_document_text(file_path),get_image_text(file_path)
    if media=='document': return get_document_text(file_path)
    if media=='image': return get_image_text(file_path)
    return '{} is an invalid media option'.format(media)