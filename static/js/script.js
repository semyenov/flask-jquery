$(function() {
	setInterval(getUpdate, 1000); // 1 second

	$('#form button').bind('click', getSend);
	$('textarea[name="text"]').keydown(function (event) {
		if (event.ctrlKey && event.keyCode == 13) {
			var button = $('button');
			if (!button.hasClass('disabled')){
				$('#form button').click();
			};
		}
	});

	function getSend() {
		$('#form button').text('Отправляю...');
		$.ajax({
			type: 'POST',
			dataType: "json",
			timeout:8000, // 8 seconds
			url: $SCRIPT_ROOT + '/send',
			data: {
					user: $CHAT_NAME,
					text: $('textarea[name="text"]').val()
			},
		 	success: function(data) {
				console.log(data.text);
				$('#form button').text('Отправить');
				$('textarea[name="text"]').val('');
				$('#chat').append('<p class="text-right"> - me <strong><pre>'+data.text+'</pre></strong></p>');
			},
			error: function(){
				$('#chat').append('<p class="text-right"><strong>SOMETHING WRONG HAPPEND!</strong></p>');
				$('#form button').addClass('disabled');
			}
		});
		
		return false;
	}


	function getUpdate() {
		console.log('Update');
		$.ajax({
			type: 'GET',
			dataType: "json",
			url: $SCRIPT_ROOT + '/update',
			data: {user: $CHAT_NAME},
			success: function(data) {
				console.log(data.messages)
				$.each(data.messages, function(i, message){
					console.log(i, message);
					$('#chat').append('<p class="text-left">'+message.user+' - <strong><pre class="inbox">'+message.text+'</pre></strong></p>')
				})
			}
		});
	}

});