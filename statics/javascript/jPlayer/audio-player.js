$(function() {
	if (/\b(iPhone|iPad|Android)\b/.test(navigator.userAgent)) {
		return;
	}
	
	var mediaList = {};
	$("#player audio source").each(function() {
		var src = $(this).attr("src");
		var m;
		if (m = src.match(/\.(\w+)$/)) {
			var ext = m[1];
			mediaList[ext] = src;
		}
	});
	$("#player audio").remove();
	
	$("#player").append(
		'<div class="jp-audio jp-type-single">' +
			'<div id="jp-interface" class="jp-interface">' +
				'<ul class="jp-controls">' +
					'<li><a href="#" class="jp-play" tabindex="1">Play</a></li>' +
					'<li><a href="#" class="jp-pause" tabindex="1">Pause</a></li>' +
					'<li><a href="#" class="jp-stop" tabindex="1">Stop</a></li>' +
					'<li><a href="#" class="jp-mute" tabindex="1">Mute</a></li>' +
					'<li><a href="#" class="jp-unmute" tabindex="1">Unmute</a></li>' +
				'</ul>' +
				'<div class="jp-progress">' +
					'<div class="jp-seek-bar">' +
						'<div class="jp-play-bar"></div>' +
					'</div>' +
				'</div>' +
				'<div class="jp-volume-bar">' +
					'<div class="jp-volume-bar-value"></div>' +
				'</div>' +
				'<div class="jp-current-time"></div>' +
				'<div class="jp-duration"></div>' +
			'</div>' +
		'</div>'
	).append(
		$('<div id="jplayer" class="jp-jplayer">').jPlayer({
			supplied: "m4a, mp3, ogg",
			solution: "html, flash",
			swfPath: "/javascript/jPlayer",
			cssSelectorAncestor: "#jp-interface",
			ready: function() {
				$(this).jPlayer("setMedia", mediaList);
			},
		})
	);
});
