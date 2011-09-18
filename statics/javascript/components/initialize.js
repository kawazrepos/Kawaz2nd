$(document).ready(function(){
	// SyntaxHighlighter
	SyntaxHighlighter.all();
	// 外部参照画像をサムネイル化する準備
	$("img[src^=http]").each(function(){
		var src = $(this).attr('src');
		if(src.indexOf == 'http://maps.gstatic.com/'){
			return;
		}else if($(this).hasClass('configured')){
			return;
		}
		var $a = $('<a>').attr({
			'href': $(this).attr('src'),
			'title': "Test",
			'rel': 'lightbox',
		});
		$(this).hide();
		$(this).addClass('auto-thumb');
		$(this).wrap($a);
		var $loading = $('<div>').addClass('loading').css({'width': '320px', 'height': '240px'});
		$(this).before($loading);
	});
});
// 外部参照画像のサムネイルか及びColorboxの適用
$(window).load(function(){
	var WIDTH = 320, HEIGHT = 240;
	$("img[src^=http].auto-thumb").each(function(){
		var $img = $(this);
		var width = $img.width();
		var height = $img.height();
		if(width > WIDTH || height > HEIGHT){
			var xoffset = width - WIDTH;
			var yoffset = height - HEIGHT;
			if(xoffset > yoffset){
				$img.width(WIDTH);
			}else{
				$img.height(HEIGHT);
			}
			$img.addClass('lightbox');
		}
		$('div.loading').remove();
		$img.fadeIn('slow');
	});
	$('a[rel=lightbox]').colorbox({'photo': true});
});
