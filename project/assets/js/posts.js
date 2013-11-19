function salvar_post () {
	var fd = new FormData($('#form-add-comment')[0]);
	$.ajax({
        url: "/crear_post/",
        data: fd,
        type: 'POST',
        success: function(data){
			window.location.assign(data.url);
        },
        error: function(data){
			var datas = $.parseJSON(data.responseText);
			$.each(datas.errores, function(index, value){
				$('.errores').append(value+"<br/>");
			});
                        $('#myModal').modal('show')
        },
        beforeSend: function(){
			$('.errores').html('');
        },
        processData: false,
        contentType: false
});
}


function edit_post(slug) {
        var fd = new FormData($('#form-add-comment')[0]);
        $.ajax({
        url: "/editar_post/"+slug+"/",
        data: fd,
        type: 'POST',
        success: function(data){
                        window.location.assign(data.url);
        },
        error: function(data){
                        var datas = $.parseJSON(data.responseText);
                        $.each(datas.errores, function(index, value){
                                $('.errores').append(value+"<br/>");
                        });
                        $('#myModal').modal('show')
        },
        beforeSend: function(){
                        $('.errores').html('');
        },
        processData: false,
        contentType: false
});
}