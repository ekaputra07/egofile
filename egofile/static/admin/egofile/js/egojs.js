function ego_randomizer() {
	var chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz";
	var string_length = 8;
	var randomstring = '';
	for (var i=0; i<string_length; i++) {
		var rnum = Math.floor(Math.random() * chars.length);
		randomstring += chars.substring(rnum,rnum+1);
	}
	return randomstring;
}

function setSingleImage(field_id, data){
    django.jQuery('#'+field_id).val(data);
    django.jQuery('#'+field_id+'_img').attr('src', data);
    django.jQuery('#add_'+field_id+' strong').text('Change Image');
}

function egofileClearValue(field_id, default_img){
    django.jQuery('#'+field_id).val('');
    django.jQuery('#'+field_id+'_img').attr('src', default_img);
    django.jQuery('#delete_'+field_id).remove();
    django.jQuery('#add_'+field_id+' strong').text('Add Image');
    return false;
}
