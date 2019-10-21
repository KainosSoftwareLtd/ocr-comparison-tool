from boto3 import client

def encode_image(file_path):
    return open(file_path,'rb').read()

def get_document_obj(file_path):
    model=client('textract')
    img_bytes=encode_image(file_path)
    return model.detect_document_text(Document={'Bytes':img_bytes})

def get_document_text(file_path):
    try:
        response=get_document_obj(file_path)
        arr=list(map(lambda x: x.get('Text'),response['Blocks']))
        text_uco=u' '.join(list(filter(None,arr))).strip()
        return text_uco.encode('ascii','replace').decode('utf-8') 
    except: return ''        

def get_image_obj(file_path):
    model=client('rekognition')
    img_bytes=encode_image(file_path)
    return model.detect_text(Image={'Bytes':img_bytes})

def get_image_text(file_path):
    response=get_image_obj(file_path)
    try:
        arr=list(map(lambda x: x['DetectedText'] if x['Type']=='LINE' else None,response['TextDetections']))
        text_uco=u' '.join(list(filter(None,arr))).strip()
        return text_uco.encode('ascii','replace').decode('utf-8')
    except: return ''

def aws_get_text(file_path,media='both'):
    if media=='both': return get_document_text(file_path), get_image_text(file_path)
    if media=='document': return get_document_text(file_path)
    if media=='image': return get_image_text(file_path)
    return '{} is an invalid media option'.format(media)