from .amazon_api import aws_get_text
from .google_api import gc_get_text
from .microsoft_api import ms_get_text

services=['amazon','google','microsoft']
media_types=['image','document']

def get_ocr_sw(media='both'):
    if media=='both': return ['{0}-{1}'.format(serv,media) for media in media_types for serv in services]
    return ['{0}-{1}'.format(serv,media) for serv in services]

def get_text(file_path,media='both'):
    if media=='both':
        return {'amazon-document':aws_get_text(file_path,media)[0],
                'amazon-image':aws_get_text(file_path,media)[1],
                'google-document':gc_get_text(file_path,media)[0],
                'google-image':gc_get_text(file_path,media)[1],
                'microsoft-document':ms_get_text(file_path,media)[0],
                'microsoft-image':ms_get_text(file_path,media)[1]}
    return {'amazon-{}'.format(media):aws_get_text(file_path,media),
            'google-{}'.format(media):gc_get_text(file_path,media),
            'microsoft-{}'.format(media):ms_get_text(file_path,media)}