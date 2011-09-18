/*
 * jQuery django-markitupfield.js
 */
$(document).ready(function(){
	var $textarea = $("textarea.django-markitupfield");
	$textarea.markItUp(mySettings);
	$textarea.indentable();
	$textarea.fullscreen(mySettings);
	$textarea.attachable();
	// Ctrl + Enterで投稿
	var $form = $($textarea.parents('form')[0]);
	$textarea.keyup(function(e){
		if(e.keyCode==13 && e.ctrlKey){
			if (confirm("内容を投稿してもよろしいですか？")) {
				$form.submit();
				e.preventDefault();
				return false;
			}
		}
		return true;
	});
});
