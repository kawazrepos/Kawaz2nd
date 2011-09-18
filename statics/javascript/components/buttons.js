$(document).ready(function(){
	// back-button
	$('button.back-button').click(function(){
		history.back();
		return false;
	});
	// draft-button
	$('button.draft-button').click(function(){
		var $form = $(this).parents('form');
		var $pub_state = $('select#id_pub_state');
		$pub_state.val('draft');
		$form.submit();
		return false;
	});
});