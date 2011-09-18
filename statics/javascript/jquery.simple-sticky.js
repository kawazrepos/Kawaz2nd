/**
 * @author Tanix
 */
(function($){
	// $("#(sticky-base)").sticky();s
	$.fn.sticky = function(settings){
		//settings = $.expand(true, {
		//}, settings)
		$el = $(this);
		//alert("")
		$el.css({
			"position": "absolute",
			"right": "0",
			"bottom": "0",
			"width": "300px",
			"height": "300px",
			"background-color": "#ccc",
			"border": "1px solid #ccc"
		});
		zi = 1000;
		
		addSticky = function()
		{
			offset = $el.offset();
			sticky = "<div"
			+" style='background-color:#ffff00;border:1px solid #000;position:absolute;"
			+"width:"+$el.width()
			+";height:"+$el.height()
			+";top:"+offset.top
			+";left:"+offset.left
			+"'></div>";
			
			$sticky = $(sticky)
			$el.after($sticky);
			$sticky.draggable({
				start: function(){
					$(this).css("opacity", 0.5)
				},
				stop: function(){
					$(this).css("opacity", 1.0)
				}
			})
			.bind("mousedown", mdSticky)
			.bind("mousedown", toTopSticky)
			.bind("dblclick", showTextArea)
			.focusout(hideTextArea);
			return $sticky;
		};
		
		mdSticky = function(){
			$sticky.unbind("mousedown", mdSticky)
			$sticky = addSticky();
		};
		
		toTopSticky = function()
		{
			$(this).css("z-index", ++zi)
		};
		
		showTextArea = function()
		{
			$s = $(this);//alert($s.css("background-color"))
			$s.unbind("dblclick");
			text = $s.html().replace("<br>", "\n");
			textarea = "<form style='width:100%;height:100%; position:relative;top:0;left:0;'>"
				+"<textarea style='width:100%;height:100%;background-color:transparent;border:none;'>"
				+text
				+"</textarea></form>"
			$textarea = $(textarea);
			//$("form", $s).remove();
			$s.html("");
			$s.append($textarea)
			$("textarea", $textarea).focus()
			//$s.css("opacity", 0.5)
		};
		
		hideTextArea = function()
		{
			//$(this).css("opacity", 1)
			$s = $(this);
			$s.bind("dblclick", showTextArea);
			$s.text($("textarea", this).val());
			$s.html($s.text().replace("\n", "<br />"));
			$("form", this).remove();
			
		};
		
		$sticky = addSticky();
		return this;
	};
})(jQuery);