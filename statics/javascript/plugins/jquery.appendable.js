/*
 * Select要素に新規項目を追加するためのjQueryプラグイン
 * 
 */
(function($){
	$.fn.appendable = function(settings){
		settings = $.extend({
			postUrl: 'required',
			buttonClass: 'addCategoryButton',
			windowClass: 'addCategoryWindow',
			message: "追加したい要素を入力してエンターを押してください"
		}, settings);
		// 表示するモーダルウィンドウを作成
		function createModalWindow($select){
			var $window = $('<div>').addClass(settings.windowClass);
			var $input = $('<input>');
			var $results = $('<ul>');
			$window.append('<h1>' + settings.message + '</h1>');
			$window.append($input);
			$window.append('<p>編集に戻るにはフォーム以外の部分をクリックしてください</p>');
			$window.append($results);
			$window.appendTo($(document));
			// Events
			$input.keypress(function(e){
				if (e.keyCode == 13) {
					$.post(settings.postUrl, {
						label: $input.val(),
						method: 'json',
					}, function(data){
						if (data.status == 'ok') {
							var $option = $('<option>').val(data.instance.pk).html(data.instance.label);
							var $result = $('<li>').html("「" + data.instance.label + "」が追加されました");
							$select.append($option);
							$results.append($result);
							$option.show();
							$result.show('fast');
							$input.val('');
						}
					}, 'json');
					return false;
				}
			});
			return $window;
		};
		function createDisplayButton($window){
			var $button = $("<a>").addClass(settings.buttonClass);
			$button.attr('href', 'javascript:void(0)');
			$button.click(function(){
				$window.lightbox_me({
					'centered': true,
					'onLoad': function(){
						$('input', $window).focus();
					}
				});
				return false;
			});
			return $button;
		};
		var $window = createModalWindow($(this));
		var $button = createDisplayButton($window);
		$(this).after($button.show());
		//$(this).width($(this).width() - $button.width() - 5);
		$(this).width($(this).width() - 21);
	};
})(jQuery);