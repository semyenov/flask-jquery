$(function() {
	$('button').bind('click', function() {
		$.getJSON($SCRIPT_ROOT + '/save', {
			name: $('input[name="dog-name"]').val(),
			b: $('input[name="b"]').val()
		}, function(data) {
			alert(data.name);
		});
		return false;
	});
});