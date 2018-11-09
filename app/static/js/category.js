$(document).ready(function() {

	$('form').on('submit', function(event) {

		$.ajax({
			data : {
				category : $('#category').val()
							},
			type : 'POST',
			url : '/category_filter'
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
