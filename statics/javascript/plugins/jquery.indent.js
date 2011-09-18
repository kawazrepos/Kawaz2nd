/**
 * @author Tanix
 */

(function($){
	function indentable(event){
		// return to do ordinary behavior unless a tab key is pressed
		if (event.keyCode !== 9) {
			return true;
		}
		
		$el = $(this);
				
		event.preventDefault();
		event.stopPropagation();
		
		var o = $el.get(0);
		o.focus();
		
		if ($.browser.msie) {
			var r = document.selection.createRange();
			var s = r.text;
			// indent lines
			if (!event.shiftKey) {
				r.text = ("\t" + s.replace(/\n/g, "\n\t")).replace(/\t\r\n/g, "\r\n");
				
				r.select();
			}
			// unindent selected lines
			else {
				s = s.replace(/\n\t/g, "\n");
				if (s.substr(0, 1) == "\t") {
					s = s.substr(1, s.length - 1);
				}
				r.select();
			}
		}
		else {
			var p = o.selectionStart;
			var e = o.selectionEnd;
			var s = o.value.substr(p, e - p);
			var head = o.value.substr(0, p);
			var tail = o.value.substr(e, o.value.length);
			
			var top = o.scrollTop;//alert(top)
			
			// simply enter a tab character when no characters are selected
			if (p == e) {
				if (!event.shiftKey) {
					$el.enterTabCharacter();
				}
				else {
					if (o.value.substr(p - 1, 1) == "\t") {
						head = head.substr(0, p - 1);
						tail = o.value.substr(p, o.value.length);
						o.value = head + tail;
						o.setSelectionRange(p - 1, p - 1);
					}
					else 
						if (o.value.substr(p, 1) == "\t") {
							head = head.substr(0, p);
							tail = o.value.substr(p + 1, o.value.length);
							o.value = head + tail;
							o.setSelectionRange(p, p);
						}
				}
			}
			else {
				//indent lines
				if (!event.shiftKey) {
					s = s.replace(/\n/g, "\n\t");
					if (s.substr(s.length - 1, 1) == "\t") {
						s = "\t" + s.substr(0, s.length - 2) + "\n";
					}
					else {
						s = "\t" + s;
					}
					s = s.replace(/\t\n/g, "\n");
				}
				// unindent lines
				else {
					s = s.replace(/\n\t/g, "\n");
					if (s.substr(0, 1) == "\t") {
						s = s.substr(1, s.length - 1);
					}
				}
				var l = s.length;
				o.value = head + s + tail;
				o.setSelectionRange(p, p + l);
			}
			//o.scrollTop = top;
			//o.focus();
		}
		//return true;
	}
	
	function autoIndentable(event)
	{
		if ($.browser.msie) {
			return true;
		}
		
		if (event.keyCode === 13) {
		
			event.preventDefault();
			event.stopPropagation();
			
			var o = $(this).get(0);
			o.focus();
			
			var p = o.selectionStart;
			var text = o.value;
			var lineStart = text.lastIndexOf("\n", p - 1) + 1;
			var lineEnd = p;
			
			if (lineStart < 0) {
				lineStart = 0;
			}
			
			var matches = text.substring(lineStart, lineEnd).match(/^([ \t]+)/);
			
			// ensure matching substring RegExp.$1 to be set
			var spaces = matches === null ? "" : RegExp.$1;
			
			// insert '\n' additionally at first and spaces at the head of the current line subsequently
			$(this).insertAtCaret("\n" + spaces);
			//o.focus();
			//return false;
		}
	}
	
	$.fn.indentable = function(settings){
		settings = $.extend(true, {
			autoIndent: true
		}, settings);
		
		return this.each(function(){
			if (settings.autoIndent) {
				$(this).autoIndentable();
			}
			
			$(this).unbind("keydown", indentable)
			.keydown(indentable);
		});
		
	};
	
	$.fn.disableIndentable = function(){
		return this.each(function(){
			$(this).unbind("keydown", indentable)
			.unbind("keydown", autoIndentable);
		});
	}
	
	$.fn.autoIndentable = function(){
		return this.each(function(){
			$(this).unbind("keydown", autoIndentable)
			.keydown(autoIndentable);
		});
	};
	
	$.fn.enableEntryTab = function(){
		return this.each(function(){
			$(this).keydown(function(event){
				if (event.keyCode === 9) {
					event.preventDefault();
					event.stopPropagation();
					$(this).enterTabCharacter();
					//return false;
				}
			});
		});
	};
	
	$.fn.enterTabCharacter = function(){
		return this.each(function(i){
			$(this).insertAtCaret("\t");
		});
	};
	
	// thanks to http://d.hatena.ne.jp/okinaka/20090727/1248671860
	$.fn.insertAtCaret = function(v){
		var o = this.get(0);
		o.focus();
		if (jQuery.browser.msie) {
			var r = document.selection.createRange();
			r.text = v;
			r.select();
		}
		else {
			var s = o.value;
			var p = o.selectionStart;
			var np = p + v.length;
			o.value = s.substr(0, p) + v + s.substr(p);
			o.setSelectionRange(np, np);
		}
		return this;
	};
})(jQuery);