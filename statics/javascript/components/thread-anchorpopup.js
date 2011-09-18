$(document).ready(function(){
	function getBody($element){
		if($element.hasClass("comment")){
			return $element.find(".comment-body");
		}else if($element.hasClass("thread")){
			return $element.find(".thread-body");	
		}
	};
	var regex = new RegExp("&gt;&gt;(\\d+)", 'gi');
	$(".response").each(function(){
		var $body = getBody($(this));
		$body.html($body.html().replace(regex, '<span class="anchor" response_number="$1">$&</span>'));
		$("span.anchor", $body).each(function(){
			var response_number = $(this).attr('response_number');
			var $response = $(".response[response_number="+response_number+"]");
			if ($response.length > 0) {
				$(this).qtip({
					content: getBody($response),
					show: 'mouseover',
					hide: 'mouseout',
					style: {
						border: {
							radius: 5
						},
						width: {
							max: 800
						}
					}
				});
				$(this).click(function(){
					location.href = "#" + $response.attr('id');
					return false;
				});
			}else{
				// 参照先が存在しないので属性を外す
				$(this).removeClass('anchor');
			}
		});
	});
});
