$(document).ready(function() {

	$('form').on('submit', function(event) {

		$.ajax({
			data : {
				priority : $('#priority').val()
							},
			type : 'POST',
			url : '/priority'
		})
		.done(function(data) {

			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
				$('#successAlert').text(data.name).show();
				$('#errorAlert').hide();
			}

		});

		event.preventDefault();

	});

});
