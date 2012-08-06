var ajax_response;
var current_path;

jQuery(document).ready(function(){
    //Run at first Load
    browsedir('');
});

function browsedir(path){
    jQuery('.loadingfile').show();
    load_breadcrumb(path);
    window.current_path = path;
    jQuery('#current_path').val(path);
    jQuery.ajax({
        url : ajaxurl,
        type : 'post',
        data : ({'csrfmiddlewaretoken': csrftoken, 'path': path}),
        success : function(response){
        window.ajax_response = response
        jQuery('.filetable tr').remove();
        for (file in response){
            if (response[file].ext == 'dir'){
            var html = dir_template(response, file);
            jQuery('.filetable').append(html);
            }else{
            var html = file_template(response, file);
            jQuery('.filetable').append(html);
            }
          }
        jQuery('.loadingfile').hide();
        },
        error : function(){
            alert('Failed retreive directory content list.');
        }
    });
    return false;
    }

function startUpload(){
    var status = jQuery('.upload-status');
    status.html('<img src="'+staticpath+'egofile/images/loading.gif"/> Uploading, please wait...');
}

function upload_response(response){
			        res = response.split('#');
			        var status = jQuery('.upload-status');

                  if(res[0] == 'error'){
                        status.html('<p style="color:red;">'+res[1]+'</p>');
                    }else{
                        status.html('<p style="color:green;">'+res[1]+'</p>');
                        status.find('p').animate({opacity:0}, 5000, function(){$(this).remove();});
                        browsedir(window.current_path);
                    }
			    }

function load_breadcrumb(path){
    jQuery.ajax({
        url : ajaxbreadcrumb,
        type :'get',
        data : ({'path': path, 'csrfmiddlewaretoken':csrftoken}),
        success : function(response){
        jQuery('.breadcrumb_ul').html(response);
        show_detail('reset'); //reset file info
        },
        error :function(){
        alert('Failed loading media breadcrumb.');
        }
    });
}

//NEED MORE DEVELOPMENT
function show_detail(file_id){
    if(file_id != 'reset'){
    file = window.ajax_response[file_id]
    jQuery('.fname').text(file.file);
    jQuery('.fsize').text(file.size);
    var file_url = window.media_url+file.url;
    jQuery('.furl').html('<a href="'+file_url+'">'+file_url+'</a>');
    if(file.ext == '.jpg' || file.ext == '.png' || file.ext == '.jpeg' || file.ext == '.gif'){
    jQuery('.fimg').html('<img src="'+file_url+'" width="250" />');
    }else{
    jQuery('.fimg').text('');
    }
    jQuery('.fext').text(file.ext);
        if(window.mode == 'popup' || window.mode == 'tinymce'){
        jQuery('.finsert').html('<input type="button" value="Insert" class="btn-dark" onclick="insert_file(\''+file.url+'\');"/>');
        }
    }else{
    jQuery('.fname').text('');
    jQuery('.fsize').text('');
    jQuery('.furl').text('');
    jQuery('.fimg').text('');
    jQuery('.fext').text('');
    jQuery('.finsert').text('');
    }
    return false;
}

//Create folder ajax
function new_folder(){
    var folder = prompt('Folder name?','');
    if(folder == ''){
        alert('Folder name please!');
        return false;
        }else if(folder==null){
        return false;
        }else{

        jQuery.post(newurl, {'csrfmiddlewaretoken':csrftoken,'folder':folder, 'current_path':window.current_path}, function(response){
            res = response.split('#');
            if(res[0] == 'error'){
                alert(res[1]);
            }else{
                alert(res[1]);
                browsedir(window.current_path);
            }
        });

        }
    }

//Rename file ajax
function rename(current_name){
    var newname = prompt('Rename "'+current_name+'" to?','');
    if(newname == ''){
        alert('New name please!');
        return false;
        }else if(newname == null){
        return false;
        }else{

        jQuery.post(renameurl, {'csrfmiddlewaretoken':csrftoken,'current_name': current_name, 'new_name':newname,'current_path':window.current_path}, function(response){
            res = response.split('#');
            if(res[0] == 'error'){
                alert(res[1]);
            }else{
                alert(res[1]);
                browsedir(window.current_path);
            }
        });

        }
    }

//Delete File ajax
function delete_file(fname, fpath){
    if (confirm('Are you sure want to delete "'+fname+'"?')){
    jQuery.post(delurl, {'csrfmiddlewaretoken':csrftoken,'path':fpath}, function(response){
        res = response.split('#');
        if(res[0] == 'error'){
            alert(res[1]);
        }else{
            alert(res[1]);
            browsedir(window.current_path);
        }

    });
    }
}

function mySubmit(furl) {
        var URL = window.media_url+furl;
        var win = tinyMCEPopup.getWindowArg("window");

        // insert information now
        win.document.getElementById(tinyMCEPopup.getWindowArg("input")).value = URL;

        // are we an image browser
        if (typeof(win.ImageDialog) != "undefined") {
            // we are, so update image dimensions...
            if (win.ImageDialog.getImageData)
                win.ImageDialog.getImageData();

            // ... and preview if necessary
            if (win.ImageDialog.showPreviewImage)
                win.ImageDialog.showPreviewImage(URL);
        }
        // close popup window
        tinyMCEPopup.close();
}

function insert_file(furl){
    if (window.mode == 'popup'){
        window.opener.egofile_do_actions(window.func_name, window.field_id, furl);
    }else if(window.mode == 'tinymce'){
        mySubmit(furl);
    }
}

/* HTML TEMPLATE PARSER*/
function dir_template(response, file_id){
    file = response[file_id];
    return '<tr>\
    <td width="1%"><a href="#" onclick="return browsedir(\''+file.path+'\');"><img src="'+staticpath+'egofile/images/folder.png" width="16" height="16"/></a></td>\
    <td width="25%"><a href="'+file.path+'" class="dir file_item" onclick="return browsedir(\''+file.path+'\');">'+file.file+'</a></td>\
    <td><div class="file-action"><a href="javascript:void(0);" title="Rename" onclick="rename(\''+file.file+'\');">Rename</a> | <a href="javascript:void(0);" title="Delete" onclick="delete_file(\''+file.file+'\',\''+file.path+'\')">Delete</a></div></td>\
    </tr>';
}

function file_template(response, file_id){
    file = response[file_id];
    ext = file.ext;
    if(ext == '.jpg' || ext == '.jpeg' || ext == '.png' || ext == '.gif'){
        var icon = staticpath+'egofile/images/picture.png';
    }else{
        var icon = staticpath+'egofile/images/file.png';
    }
    return '<tr>\
    <td width="1%"><img src="'+icon+'" width="16" height="16"/></td>\
    <td width="25%"><a href="'+file.url+'" class="file file_item" onclick="return show_detail('+file_id+');">'+file.file+'</a></td>\
    <td><div class="file-action"><a href="javascript:void(0);" title="Rename" onclick="rename(\''+file.file+'\');">Rename</a> | <a href="javascript:void(0);" title="Delete" onclick="delete_file(\''+file.file+'\',\''+file.path+'\')">Delete</a></div></td>\
    </tr>';
}

