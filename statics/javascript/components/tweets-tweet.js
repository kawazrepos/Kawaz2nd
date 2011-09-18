/*
 * Tweets Application Javascript
 * 
 * Author:	Alisue
 * Date:	2010/10/10
 * 
 */
//(function($){
function favoriteTweet(url, object_id){
	var $tweet = $('#tweet-'+object_id).closest('li.tweet');
	var $button = $('.favorite-button', $tweet);
	var $favorites = $tweet.find(".tweet-favorites");
	$.post(url, {'object_id': object_id}, function(data){
		user = data.user;
		if (data.action == 'add') {
			$button.removeClass('add');
			$button.addClass('delete');
			$tweet.addClass('tweet-favorite');
			$user = $("<li>").addClass('favorite-user').attr('id', 'favorite-user'+user.pk).append($('<a>').attr({'href':user.href,'alt':user.username}).append($(user.icon)));
			$favorites.append($user.toggle(false));
			$user.ready(function(){
				$user.toggle('slow');
			});
		} else {
			$button.removeClass('delete');
			$button.addClass('add');
			$tweet.removeClass('tweet-favorite');
			$favorites.children("li#favorite-user"+user.pk).toggle('slow', function(){
				$(this).remove();
			});
		}
	}, 'json');
}
function reTweet(tweet_id, user_id, tweet_body){
	$('#id_reply').val(tweet_id);
	var body = $('#id_body').val();
	var reply = "@" + user_id;
	$('#id_body').val(body+"RT"+" "+reply+" "+tweet_body).keydown(function(e){
		if($(this).val().indexOf(reply) == -1){
			// @<user_id>が消去されたのでリプライ情報を抹消
			$('#id_reply').val("");
		}
	});
	var $tweet_form = $('#tweet-form');
	$tweet_form.show('fast');
}
function replyTweet(tweet_id, user_id){
	$('#id_reply').val(tweet_id);
	var body = $('#id_body').val();
	var reply = "@" + user_id;
	$('#id_body').val(reply+" "+body).keydown(function(e){
		if($(this).val().indexOf(reply) == -1){
			// @<user_id>が消去されたのでリプライ情報を抹消
			$('#id_reply').val("");
		}
	});
	var $tweet_form = $('#tweet-form');
	$tweet_form.show('fast');
}
function deleteTweet(url){
	if (window.confirm("ツイートの削除は取り消せません。このツイートを削除してもよろしいですか？")){
		$.post(url, function(){
			location.href = location.href;
		});
	}
}
function hideTweetTools(){
	// tweet-toolsを不可視に
	var $tweet_tools = $('div.tweet-tools');
	$tweet_tools.hide();
	var $tweet = $('li.tweet');
	$tweet.hover(function(){
		$('div.tweet-tools', $(this)).show();
	}, function(){
		$('div.tweet-tools', $(this)).hide();
	});
}
$(document).ready(function(){
	hideTweetTools();
	// ツイート領域を可変に
	var $tweet_form = $('#tweet-form');
	var $tweet_body = $('textarea', $tweet_form);
	var $tweet_submit = $('input', $tweet_form);
	$tweet_submit.hide();
	$tweet_body.css({'height': '2em'});
	$tweet_body.focus(function(){
		$tweet_body.css({'height': '4em'});
		$tweet_submit.show();
	});
	/*$tweet_body.blur(function(){
		$tweet_body.css({'height': '2em'});
		$tweet_submit.hide();
	});*/
	// Enterでツイート可能に
	$tweet_body.keydown(function(e){
		if (e.keyCode == 13){	// Enter
			$tweet_form.submit();
			return false;
		}
	});
	// Validation
	$tweet_form.submit(function(){
		if ($tweet_body.val() == ''){
			return false;
		}
	});
	// Readmore実装
	var twitter_current_loading_page=2;
	$("p.tweet-more").click(function(){
		$readmore = $(this);
		$loading = $("<p>").addClass("loading").text("loading...");
		var $tweets = $("ul.tweets");
		$(this).before($loading);
		var $link = $(this).find("a");
		var url = $link.attr('href');
		$.get(url, {'page': twitter_current_loading_page}, function(data){
			var $page = $(data);
			$link.attr('href', url);
			var $new = $page.find("li.tweet");
			$tweets.append($new);
			$new.fadeOut(0);
			hideTweetTools();
			twitter_current_loading_page++;
			$new.fadeIn('normal', function(){
				$next = $page.find("div.pagination a.next");
				$loading.remove();
				if (!$next.html()) {
					$readmore.remove();
				}
			});
		}, 'html');
		return false;
	});
});
