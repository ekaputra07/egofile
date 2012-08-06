from django import template
from django.utils.safestring import mark_safe

from egofile.utils import file_root_from_url, egoformat_to_list

register = template.Library()


#tags to convert file url to its server path
@register.filter
def to_path(value):
    return file_root_from_url(value)

#return list version of egoformat_string
@register.tag
def egoformat_list(parser, token):
    args = token.split_contents()
    
    if len(args) != 4:
        raise template.TemplateSyntaxError('egoformat_list tag usage not valid!. Usage : egoformat_to_list [egoformat_string] as [varname]')
    
    return EgoformatNode(args[1], args[3])
    
class EgoformatNode(template.Node):
    def __init__(self, string, varname):
        self.string = template.Variable(string)
        self.varname = varname
        
    def render(self, context):
        egoformat_string = self.string.resolve(context)
        context[self.varname] = egoformat_to_list(egoformat_string)
        return ''
        
