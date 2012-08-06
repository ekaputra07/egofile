from django.core.urlresolvers import reverse
from django.conf import settings
import os

def filebrowser_url(field_id, js_function):
    """
    return Django-Egofile file browser Url
    """
    return reverse('egofile_index') + '?to='+field_id+'&action_id='+js_function
    
def file_root_from_url(url):
    """
    Get full path of file in Media based on file Url
    """
    media_url = settings.MEDIA_URL
    media_root = settings.MEDIA_ROOT
    if media_url in url:
        fileobj = url.replace(media_url, media_root)
    else:
        fileobj = media_root+url
        
    fileobj = os.path.normpath(fileobj)
    return fileobj

def egoformat_to_list(string):
    """
    Convert string : abc#def#xyz
    to list : ['abc','def','xyz']
    """
    the_list = []
    if string:
        the_list = string.split('#')
    return the_list
    
    
    
