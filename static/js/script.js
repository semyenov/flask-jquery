$(function() {
	setInterval(getUpdate, 1000); // 300,000 miliseconds is 5 minutes

	$('button').bind('click', getSend);
	$('textarea[name="text"]').keydown(function (event) {
		if (event.ctrlKey && event.keyCode == 13) {
			getSend();
		}
	});

	function getSend() {
		$('button').text('Отправляю...');
		$.ajax({
			type: 'POST',
			dataType: "json",
			url: $SCRIPT_ROOT + '/send',
			data: {
					user: $CHAT_NAME,
					text: $('textarea[name="text"]').val()
			},
		 	success: function(data) {
				console.log(data.text);
				$('button').text('Отправить');
				$('textarea[name="text"]').val('');
				$('#chat').append('<p class="text-right">'+$CHAT_NAME+': <strong>'+data.text+'</strong></p>');
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
				$.each(data.messages, function(i, message){
					$('#chat').append('<p class="text-left">'+message.user+': <strong>'+message.text+'</strong></p>')
				})
			}
		});
	}

});