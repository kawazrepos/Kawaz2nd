$(document).ready(function(){
	// ムードメッセージを編集可能に
	var $mood = $('div.profile-mood.editable');
	if ($mood) {
		$mood.attr({'contenteditable': 'true'});
		$mood.keydown(function(e){
			if (e.keyCode == 13){	// Enter
				return false;
			}
		});
		$mood.blur(function(){
			// Update mood message
			$.post($mood.attr('posturl'), {'mood': $mood.html()});
		});
	}
});