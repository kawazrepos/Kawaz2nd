$(document).ready(function(){
	var setSelectImage = function(){
		var options = $(".select-service-column select option").each(function(){
			if ($(this).val()!="") {
				$(this).attr("title", "/image/serviceicons/" + $(this).val() + ".png");
			}
		});
		$(".select-service-column > select").msDropDown();
	}
	$('table#services tr').formset({
		// For inline formsets, be sure to set the prefix, as the default prefix
		// ('form') isn't correct.
		// Django appears to generate the prefix from the lowercase plural
		// name of the related model, with camel-case converted to underscores.
		prefix: 'services',
		addCssClass: 'addServiceButton',
		deleteCssClass: 'deleteServiceButton',
		addText: 'サービスを追加する',
		deleteText: '',
		added: setSelectImage
	});
	$("#id_birthday").datepicker({
		'buttonImage': '/image/icon/events.event.png',
		'changeMonth':true,
		'changeYear':true,
		'closeText':'確定',
		'dateFormat':'yy-mm-dd',
		'dayNamesMin': ['日', '月', '火', '水', '木', '金', '土'],
		'maxDate': new Date(2000, 12, 31),
		'minDate': new Date(1950, 1, 1),
		'monthNames': ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
		'monthNamesShort': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
		'nextText': '次',
		'prevText': '前',
		'showMonthAfterYear': true,
		'showButtonPanel': true,
		'yearRange': 'c-60:c'
	});
	setSelectImage();
});