from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.conf import settings
from mimetypes import guess_type
from django.utils import simplejson
from django.utils.translation import ugettext as _
import os

@login_required(login_url='/admin/')
def index(request):
    template = 'default.html'
    popup = request.GET.get('_popup','')
    if popup:
        field_id = request.GET.get('to','')
        action_id = request.GET.get('action_id','')
        types = request.GET.get('type','')
        if types == 'tinymce':
            mode = 'tinymce'
        else:
            mode = 'popup'

        data = {'mode': mode, 'field_id': field_id, 'func_name': action_id}
        template = 'popup.html'
    else:
        data = {'mode': 'browser'}

    return render_to_response('egofile/'+template, data ,context_instance= RequestContext(request))

@login_required(login_url='/admin/')
def ajax_index(request):
    if request.is_ajax():
        if request.method == 'POST':
            path = request.POST.get('path', '')
            #norm_path = os.path.normpath(path)
            contents = list_directory(path)
            return HttpResponse(simplejson.dumps(contents), mimetype='application/json')

@login_required(login_url='/admin/')
def ajax_delete(request):
    if request.is_ajax():
        if request.method == 'POST':
            path = request.POST.get('path', '')
            dirpath = settings.MEDIA_ROOT+path
            try:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(dirpath):
                    os.rmdir(dirpath)
                else:
                    pass
            except:
                return HttpResponse('error#Failed deleting file.')

            return HttpResponse('ok#File deleted successfully.')

@login_required(login_url='/admin/')
def ajax_new(request):
    if request.is_ajax():
        if request.method == 'POST':
            folder = request.POST.get('folder', '')
            current_path = request.POST.get('current_path','')
            f = settings.MEDIA_ROOT+current_path+'/'+folder
            f = os.path.normpath(f)
            try:
                os.mkdir(f)
            except:
                return HttpResponse('error#Failed creating folder "%s"' % folder )

            return HttpResponse('ok#Folder "%s" created successfully.' % folder)

@login_required(login_url='/admin/')
def ajax_rename(request):
    if request.is_ajax():
        if request.method == 'POST':
            current_path = request.POST.get('current_path','')
            file_name = request.POST.get('current_name','')
            new_name = request.POST.get('new_name','')

            file_path = settings.MEDIA_ROOT+current_path+'/'+file_name
            new_path = settings.MEDIA_ROOT+current_path+'/'+new_name
            try:
                os.rename(file_path, new_path)
            except:
                return HttpResponse('error#Failed renaming file.')

            return HttpResponse('ok#File renamed successfully.')

@login_required(login_url='/admin/')
def ajax_upload(request):

    if request.method == 'POST':
            current_path = request.POST.get('current_path','')
            upfile = request.FILES.get('file', '')

            if upfile == '':
                response = 'error#File uploading failed!'
            else:
                destination = settings.MEDIA_ROOT+'/'+current_path+'/'+upfile.name
                dest = os.path.normpath(destination)
                response = 'ok#File "%s" uploaded successfully!' % upfile.name
                try:
                    to = open(dest, 'wb+')
                    for chunk in upfile.chunks():
                        to.write(chunk)
                    to.close()
                except:
                    response = 'error#File uploading failed!'


            js = u"<script type='text/javascript'>window.parent.upload_response('%s');</script>" % response
            return HttpResponse(js)


def list_directory(path):
    path = (path+'/').lstrip('/')
    base_path = settings.MEDIA_ROOT
    base_url = settings.MEDIA_URL
    scan_path = base_path+path
    try:
        contents = os.listdir(scan_path)
        files = {}
        key = 1
        for item in contents:
            if item[:1] != '.': #avoid display hidden file type
                file_path = scan_path+item

                if os.path.isdir(file_path):
                    files[key] = {'file': item, 'path':path+item, 'url': base_url+path+item,'ext': 'dir', 'size': '-'}
                    key += 1

        for item in contents:
            if item[:1] != '.': #avoid display hidden file type
                file_path = scan_path+item

                if os.path.isfile(file_path):
                    #get mimetype
                    #mime = guess_type(file_path)[0]
                    #get file size
                    fsize = os.path.getsize(file_path)
                    #get file extension
                    ext = os.path.splitext(file_path)[1]

                    files[key] = {'file': item,'path':file_path, 'url': path+item, 'ext': ext, 'size':convert_bytes(fsize)}
                    key += 1

        return files
    except:
        return False

#http://www.5dollarwhitebox.org/drupal/node/84
def convert_bytes(bytes):
    bytes = float(bytes)
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2f Tb' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2f Gb' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2f Mb' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2f Kb' % kilobytes
    else:
        size = '%.2f b' % bytes
    return size

def generate_ajax_breadcrumb(request):
    if request.is_ajax():
        if request.method == 'GET':
            path = request.GET.get('path', '')
            html = '<li><a href="#" onclick="return browsedir(\'\');">Media / </a></li>'
            path_part = path.split('/')
            path_length = len(path_part)
            x = ''
            for p in path_part:
                if p != '' and p != '.':
                    x += p+'/'
                    if p == path_part[path_length-1]:
                        html +='<li><span>'+p+' / </span></li>'
                    else:
                        html +='<li><a href="#" onclick="return browsedir(\''+x+'\');">'+p+' / </a></li>'
                else:
                    pass

            return HttpResponse(html)

