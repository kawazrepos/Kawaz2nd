/**
 * @author Tanix
 * @inspector giginet
 * 			  alisue
 * require markitup and lightbox-me
 */
 (function($){
 	$.fn.fullscreen = function(settings, extraSettings) {
		settings = jQuery.extend({
			
		}, settings, extraSettings);
		
		function show($textarea){
			// フルスクリーン用にMarkItUpの定義を書き換える
			settings.previewAutoRefresh = true;
			settings.resizeHandle = false;
			// MarkItUpクローンを作成
			var $cloned = $textarea.clone();
			$cloned.markItUp(settings);
			$cloned.indentable();
			$cloned.attachable();
			$cloned.siblings('.markItUpHeader')
				.append("閉じるにはESCキーを押してください");
			var $container = $cloned.parents('.markItUp');
			$container.css({
				'background-color': 'white',
				position: 'fixed'
			});
			var $header = $container.find(".markItUpHeader");
			var $footer = $container.find(".markItUpFooter");
			
			var RATIO = 0.9;
			$container.width($(window).width() * RATIO);
			$container.height($(window).height() * RATIO);
			
			$cloned.val($textarea.val());
			
			$container.lightbox_me({
				centered: true,
				onLoad: function(){
					$cloned.width($container.width() - 12);
					$cloned.height($container.height() - $header.height() - $footer.height());
					/*
					 * TODO:
					 *   ここでスクロールを無効化する処理を必要とする。時間がないので後回し
					 */
				},
				onClose: function(){
					$textarea.val($cloned.val());
					$container.remove();
				}
			});
		}
		
		var $textarea = $(this);
		var $header = $('.markItUpHeader');
		if ($('.fullscreen', $header).length > 0) {
			$('li.fullscreen', $header).click(function(){
				show($textarea);
			});
		}
	};
})(jQuery);
