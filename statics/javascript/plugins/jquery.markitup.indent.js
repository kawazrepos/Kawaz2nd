/**
 * @author		Tanix
 * @inspector	alisue
 * 
 * required		jquery.markitup.js
 * 
 * はまった部分
 * 	+	`keydown`イベントだと押しっぱなしが処理できないことがある
 * 		>	`keypress`だと完璧に処理可能
 * +	スクロールが毎度トップに戻ってしまう
 * 		>	Textarea要素の値を変更すると一番上に戻るのが原因。したがって
 * 		>	変更する前にscrollTopの値をキャッシュし変更後にscrollTopの
 * 		>	値を戻す。その後`setSelectionRange`でキャレットの位置を設定する
 * 		>	という順序を踏む必要がある（一瞬だけスクロールがトップに戻るのは
 * 		>	仕方がない）
 */
(function($){
	var INDENT = "    ";
	// 全ての文字列を置き換える関数でStringを拡張
	String.prototype.replaceAll = function(src, dst){
		return this.split(src).join(dst);
	};
	// カーソル位置に文字列を挿入する関数
	$.fn.insertAtCaret = function(v){
		return this.each(function(){
			if (jQuery.browser.msie) {
				var r = document.selection.createRange();
				r.text = v;
				r.select();
			}
			else {
				// Opera対策
				$(this).get(0).focus();
				var el = $(this).get(0);
				var value = $(this).val();
				var top = el.scrollTop;
				var start = el.selectionStart;
				$(this).val(value.substr(0, start) + v + value.substr(start));
				el.scrollTop = top;
				el.setSelectionRange(start+v.length, start+v.length);
			}
		});
	};
	// Indent
	$.fn.indent = function(c){
		return this.each(function(){
			if ($.browser.msie) {
				var r = document.selection.createRange();
				var s = r.text;
				r.text = (c + s.replaceAll("\n", "\n"+c)).replaceAll(c+"\r\n", "\r\n");
				r.select();
			} else {
				// jQueryオブジェクトではないことを保証するために必須
				var el = $(this).get(0);
				var top = el.scrollTop;
				var start = el.selectionStart;
				var end = el.selectionEnd;
				var value = $(this).val();
				var str = value.substr(start, end - start);
				var head = value.substr(0, start);
				var tail = value.substr(end, value.length);
				if (start == end){
					$(this).insertAtCaret(c);
				} else {
					str = str.replaceAll("\n", "\n"+c);
					if (str.substr(str.length - c.length, c.length) == c) {
						str = c + str.substr(0, str.length - (c.length + 1)) + "\n";
					}
					else {
						str = c + str;
					}
					str = str.replaceAll(c+"\n", "\n");
					$(this).val(head + str + tail);
					el.scrollTop = top;
					el.setSelectionRange(start, start + str.length);
				}
			}
		});
	};
	// Unindent
	$.fn.unindent = function(c){
		return this.each(function(){
			if ($.browser.msie) {
				var r = document.selection.createRange();
				var s = r.text;
				s = s.replaceAll("\n"+c, "\n");
				if (s.substr(0, c.length) == c){
					s = s.substr(c.length, s.length - c.length);
				}
				r.select();
			}else{
				// jQueryオブジェクトではないことを保証するために必須
				var el = $(this).get(0);
				var top = el.scrollTop;
				var start = el.selectionStart;
				var end = el.selectionEnd;
				var value = $(this).val();
				var str = value.substr(start, end - start);
				var head = value.substr(0, start);
				var tail = value.substr(end, value.length);
				if (start == end){
					if (value.substr(start - c.length, c.length) == c){
						head = head.substr(0, start - c.length);
						tail = value.substr(start, value.length);
						$(this).val(head + tail);
						el.scrollTop = top;
						el.setSelectionRange(start - c.length, start - c.length);
					}else{
						if (value.substr(start, c.length) == c){
							head = head.substr(0, start);
							tail = value.substr(start + c.length, value.length);
							$(this).val(head + tail);
							el.scrollTop = top;
							el.setSelectionRange(start, start);
						}
					}
				} else {
					str = str.replaceAll("\n"+c, "\n");
					if (str.substr(0, c.length) == c) {
						str = str.substr(c.length, str.length - c.length);
					}
					$(this).val(head + str + tail);
					el.scrollTop = top;
					el.setSelectionRange(start, start + str.length);
				}
			}
		});
	};
	// Backspace
	$.fn.backspace = function(c){
		return this.each(function(){
			if ($.browser.msie) {
				var r = document.selection.createRange();
				var s = r.text;
				s = s.replaceAll("\n"+c, "\n");
				if (s.substr(0, c.length) == c){
					s = s.substr(c.length, s.length - c.length);
				}
				r.select();
			}else{
				// jQueryオブジェクトではないことを保証するために必須
				var el = $(this).get(0);
				var top = el.scrollTop;
				var start = el.selectionStart;
				var end = el.selectionEnd;
				var value = $(this).val();
				var str = value.substr(start, end - start);
				var head = value.substr(0, start);
				var tail = value.substr(end, value.length);
				if (start == end){
					if (value.substr(start - c.length, c.length) == c){
						head = head.substr(0, start - c.length);
						tail = value.substr(start, value.length);
						$(this).val(head + tail);
						el.scrollTop = top;
						el.setSelectionRange(start - c.length, start - c.length);
					}else{
						if (value.substr(start, c.length) == c){
							head = head.substr(0, start);
							tail = value.substr(start + c.length, value.length);
						} else {
							start -= 1;
							head = head.substr(0, start);
							tail = value.substr(start + 1, value.length);
						}
						$(this).val(head + tail);
						el.scrollTop = top;
						el.setSelectionRange(start, start);
					}
				} else {
					str = '';
					$(this).val(head + str + tail);
					el.scrollTop = top;
					el.setSelectionRange(start, start + str.length);
				}
			}
		});
	};
	// TABキー・Ctrl+>によるインデントおよび
	// Shift+TAB・Ctrl+<によるアンインデントを有効化するためのコールバック
	// またBackSpaceによるアンインデントも実装済み
	function tabIndentCallback(e){
		var TAB = 9;
		var BACKSPACE = 8;
		var LEFT = $.browser.safari ? 188 : 44;
		var RIGHT = $.browser.safari ? 190 : 46;
		// 指定キー以外は受け付けない
		if (e.keyCode !== TAB && e.keyCode !== BACKSPACE && !(e.which === LEFT && e.ctrlKey) && !(e.which === RIGHT && e.ctrlKey)){
			return true;
		}
		// Operaの為に必須
		$(this).get(0).focus();
		// イベントキャンセル
		e.preventDefault();
		e.stopPropagation();
		
		if (e.keyCode === BACKSPACE){
			$(this).backspace(INDENT);
		}else if ((e.keyCode === TAB && e.shiftKey) || (e.which === LEFT && e.ctrlKey)){
			$(this).unindent(INDENT);
		}else{
			$(this).indent(INDENT);
		}
		return false;
	}
	// Enterキーでオートインデント（タブおよびスペース対応）を有効化するためのコールバック
	function autoIndentCallback(e){
		// Enter以外は受け付けない
		if (e.keyCode !== 13){
			return true;
		}
		// IEでは実装不可能なためキャンセル
		if ($.browser.msie) {
			return true;
		}
		// Operaの為に必須
		$(this).get(0).focus();
		// イベントキャンセル
		e.preventDefault();
		e.stopPropagation();
		// 選択範囲
		var el = $(this).get(0);
		var top = el.scrollTop;
		var value = $(this).val();
		var start = el.selectionStart;
		var end = el.selectionEnd;
		var lineStart = value.lastIndexOf("\n", start - 1) + 1;
		lineStart = lineStart < 0 ? 0 : lineStart;
		var lineEnd = start;
		var regex = new RegExp("^([ \t]+)");
		var matches = value.substring(lineStart, lineEnd).match(regex);
		// RegExp.$1がセットされていない場合変な値が入るためマッチが見つからなかった
		// 場合には空文字を返すようにする
		var spaces = matches === null ? "" : RegExp.$1;
		// 見つかった分だけインデントを行う
		$(this).insertAtCaret("\n"+spaces);
		this.scrollTop = this.scrollHeight;
	}
	// 対象オブジェクト（Textarea）でTABによるインデントを有効化
	$.fn.indentable = function(settings){
		settings = $.extend({
			autoindent: false,
			markItUpHeaderClass: 'markItUpHeader',
			indentableClass: 'indentable',
			disindentableClass: 'disindentable',
			indentableTitle: "インデントを有効化"
		}, settings);
		return this.each(function(){
			// ブラウザによりバインドするイベントを変更
			if ($.browser.safari) {
				// Webkit系は`keydown`イベントが押しっぱなしでも発生
				// また`keypress`では動作せず。したがって`keydown`
				// を利用する
				$(this).bind('keydown', tabIndentCallback, false);
			}
			else {
				// `keydown`だと一度しか実行されないので`keypress`を使う
				// また第三引数を`false`にすることで「イベントバブリング方式
				// でイベントを伝播させるようにしている
				$(this).bind('keypress', tabIndentCallback, false);
			}
			if (settings.autoindent) {
				if($.browser.safari){
					$(this).bind('keydown', autoIndentCallback, false);
				}
				else{
					$(this).bind('keypress', autoIndentCallback, false);
				}
				
			}
			// MarkItUp Editorの場合は無効ボタンを実装
			var $header = $("."+settings.markItUpHeaderClass);
			if ($("."+settings.disindentableClass, $header).length > 0) {
				var $textarea = $(this);
				$('li.' + settings.disindentableClass, $header)
				.unbind("click")
				.click(function(){
					$(this).removeClass(settings.disindentableClass)
						.addClass(settings.indentableClass)
						.children().attr('title', settings.indentableTitle);
					$textarea.disindentable(settings);
					return false;
				});
			}
		});
	}
	// 対象オブジェクト（Textarea）でTABによるインデントを無効化
	$.fn.disindentable = function(settings){
		settings = $.extend({
			autoindent: false,
			markItUpHeaderClass: 'markItUpHeader',
			indentableClass: 'indentable',
			disindentableClass: 'disindentable',
			disindentableTitle: "インデントを無効化"
		}, settings);
		return this.each(function(){
			if (jQuery.browser.safari) {
				$(this).unbind('keydown', tabIndentCallback);
			}
			else {
				$(this).unbind('keypress', tabIndentCallback);
			}
			if (settings.autoindent) {
				if($.browser.safari){
					$(this).unbind('keydown', autoIndentCallback);
				}
				else{
					$(this).unbind('keypress', autoIndentCallback);
				}
			}
			// MarkItUp Editorの場合は有効ボタンを実装
			var $header = $("."+settings.markItUpHeaderClass);
			if ($("."+settings.indentableClass, $header).length > 0) {
				var $textarea = $(this);
				$('li.' + settings.indentableClass, $header)
				.unbind("click")
				.click(function(){
					$(this).removeClass(settings.indentableClass)
						.addClass(settings.disindentableClass)
						.children().attr('title', settings.disindentableTitle);
					$textarea.indentable(settings);
					return false;
				});
			}
		});
	}
})(jQuery);
