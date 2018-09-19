function rgb2hex(rgb) {
    if (/^#[0-9A-F]{6}$/i.test(rgb)) return rgb;

    rgb = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
    function hex(x) {
        return ("0" + parseInt(x).toString(16)).slice(-2);
    }
    return "#" + hex(rgb[1]) + hex(rgb[2]) + hex(rgb[3]);
}


var colHEX=''

$(function(){
	$(".form-wrapper:input").click(function(){
		try 
		{	
			if (colHEX=='')
			{
				var colRGB = $(this).css("background-color");
				colHEX = '#FFFFFF';
			}
		}
		catch(err)
		{
			alert(err.message);
		}
		
	});

	$(".form-wrapper:input").focusin(function(){
		
		$(this).css('background-color','yellow');
	});

	$(".form-wrapper:input").focusout(function(){
		$(this).css('background-color', colHEX);
		colHEX='';
	});
});
