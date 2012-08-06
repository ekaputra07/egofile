from django.forms import TextInput
from django.forms.util import flatatt
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template.loader import render_to_string

from utils import filebrowser_url, file_root_from_url
from settings import INSTALLED_JS

class SingleImageWidget(TextInput):
    class Media:
        js = INSTALLED_JS
    
    def render(self, name, value, *args, **kwargs):
        #form = super(SingleImageWidget, self).render(name, value, *args, **kwargs)
        
        filebrowser = filebrowser_url(name, 'setMultipleImage_'+name)
        
        image_list = []
        if value:
            image_list = [value]
            
        data = {
            'STATIC_URL' : settings.ADMIN_MEDIA_PREFIX,
            'name' : name,
            'filebrowser_url' : filebrowser,
            'images' : image_list, 
            'is_single': True,
            'value': value,
        }
        
        custom_output = render_to_string('egofile/multi_image_widget.html', data)
        
        return mark_safe(custom_output)
        
class MultiImageWidget(TextInput):
    class Media:
        js = INSTALLED_JS
    
    def render(self, name, value, *args, **kwargs):
        #form = super(MultiImageWidget, self).render(name, value, *args, **kwargs)
        
        filebrowser = filebrowser_url(name, 'setMultipleImage_'+name)
        
        image_list = []
        if value:
            image_list = value.split('#')
            
        data = {
            'STATIC_URL' : settings.ADMIN_MEDIA_PREFIX,
            'name' : name,
            'filebrowser_url' : filebrowser,
            'images' : image_list,
            'value': value,
        }
        
        custom_output = render_to_string('egofile/multi_image_widget.html', data)
        
        return mark_safe(custom_output)
