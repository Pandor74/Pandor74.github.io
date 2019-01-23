
$(function(){
    

    $("*.p_detail").hide(0);


	$(".plus").click(function(){
        
        $(this).parent().parent().next(".detail_pers").toggle("drop");

        var val = $(this).text();


        if (val == "+") {
        	$(this).text("-");
        }
        else {
        	$(this).text("+");
        };
    


    });


    });



