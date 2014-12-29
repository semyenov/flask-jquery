$(function() {
	$('button').bind('click', function() {
		$(this).text('Отправляю...');
		$.getJSON($SCRIPT_ROOT + '/send', {
			user: $CHAT_NAME,
			text: $('textarea[name="text"]').val()
		}, function(data) {
			console.log(data.text);
			$('button').text('Отправить');
			$('textarea[name="text"]').val('');
		});
		return false;
	});
});