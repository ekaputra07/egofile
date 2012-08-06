from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('egofile.views',
    url(r'^files/$', 'index', name='egofile_index'),
    url(r'^files/ajax/$', 'ajax_index', name='egofile_ajax'),
    url(r'^files/ajax/del/$', 'ajax_delete', name='egofile_ajaxdelete'),
    url(r'^files/ajax/new/$', 'ajax_new', name='egofile_ajaxnew'),
    url(r'^files/ajax/rename/$', 'ajax_rename', name='egofile_ajaxrename'),
    url(r'^files/ajax/upload/$', 'ajax_upload', name='egofile_ajaxupload'),
    url(r'^files/breadcrumb/$', 'generate_ajax_breadcrumb', name='egofile_breadcrumb'),
)

