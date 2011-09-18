function toggleAdvertisement(){
	$("#advertisement").fadeOut("fast");
	$.cookie("advertisement-hide", 1);
}
$(document).ready(function(){
	if(!$.cookie("advertisement-hide")){
		$("#advertisement").show('fast');
	}
});