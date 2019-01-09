
$(function(){
    
    $("*.detail_lot").hide(0);

	$(".plus").click(function(){
        
        $(this).parent().parent().next(".detail_lot").toggle("drop");

        var val = $(this).text();


        if (val == "+") {
        	$(this).text("-");
        }
        else {
        	$(this).text("+");
        };
       
        
    	});

    });


