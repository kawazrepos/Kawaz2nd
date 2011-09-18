(function($){
	$.fn.attachable = function(settings){
		settings = $.extend({
			postUrl:		'/commons/attache/',
			buttonClass:	'attacheButton',
			windowClass:	'attacheWindow'
		}, settings);

		function getModalWindow($body){
			var $window = $('<div>').addClass(settings.windowClass);
			var $input = $('<input>').attr({type: 'file', id: 'id_file', name: 'file'});
			var $results = $('<ul>');
			$input.change(function(){
				$input.upload(settings.postUrl, function(data){
					if (data.status == 'ok'){
						$body.val($body.val() + "\n" + data.instance.tag + "\n");
						var $new_item = $('<li>').html("「<a href='" + data.instance.url + "' target='_blank'>" + data.instance.filename + "</a>」を追加しました");
						$results.append($new_item);
						$new_item.show('fast');
						$input.val('');
					} else {
						alert(data.errors);
						alert("エラーが発生したためファイルの追加ができませんでした。開発者にお問い合せください");
					}
				}, 'json');
			});
			$window.append('<h1>添付ファイルを追加</h1>');
			$window.append('<p>ここで添付したファイルはデフォルトでダウンロード不可となります。<br />ダウンロードを可能にするには添付後にライセンスの設定を変更してください</p>');
			$window.append($input);
			$window.append('<p>編集に戻るにはフォーム以外の部分をクリックしてください');
			$window.append($results);
			$window.appendTo($(document));
			return $window;
		}
		
		function getAttacheButton($window){
			var $button = $('<a>').addClass(settings.buttonClass)
				.text('添付ファイルを追加')
				.attr('title', "添付ファイル")
				.attr('href', 'javascript:void(0)')
				.css('cursor', 'pointer')
				.click(function(){
					$window.lightbox_me({
						'centered': true,
						'onLoad': function(){$('input', $window).focus();}
					});
				});
			return $button;
		}
		
		return this.each(function(){
			var $window = getModalWindow($(this));
			var $header = $('.markItUpHeader');
			if ($('.attache', $header).length > 0) {
				$('li.attache', $header).click(function(){
					$window.lightbox_me({
						centered: true,
						onLoad: function(){
							$('input', $window).focus();
						}
					});
				});
			}
			else {
				var $attacheButton = $("<li>").addClass('markItUpButton').addClass('attacheButton').append(getAttacheButton($window));
				$(this).append($attacheButton);
			}
		});
	};
})(jQuery);