/*
 * messages
 */
$(document).ready(function(){
	// メッセージが存在する場合はフェードインさせて指定時間後にフェードアウトする
	var $messages = $('#messages');
	if ($messages) {
		$messages.fadeIn(500);
		setTimeout(function(){
			$messages.fadeOut(500, function(){
				$messages.remove();
			});
		}, 3000);
	}
});