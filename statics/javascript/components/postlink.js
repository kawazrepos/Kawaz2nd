/*
 * Django風の`<model>_confirm_delete.html`をワンタイムで行うためのJavaScript
 * 
 * Attr:
 *   confirm_message - 指定されている場合はクリックしたときに確認メッセージを表示する
 *   success_message - 指定されている場合はクリックしたときに成功メッセージを表示する
 */
$(document).ready(function(){
	$('a.postlink').each(function(){
		$(this).click(function(){
			var url = $(this).attr('href');
			var confirm_message = $(this).attr('confirm_message');
			var success_message = $(this).attr('success_message');
			var success_callback = $(this).attr('success_callback');
			if(confirm_message != undefined && !confirm(confirm_message)){
				return false;
			}
			$.post(url, function(){
				if(success_message != undefined){
					alert(success_message);
				}
				if(success_callback != undefined){
					eval(success_callback);
				}else{
					location.href = location.href;
				}
			});
			return false;
		});
	});
});
