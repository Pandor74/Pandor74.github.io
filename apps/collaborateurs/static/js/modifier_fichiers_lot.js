








$(function(){
    $("#p2").click(function(){
        
        $("#fl2").show();
        $("#p2").hide();
        $("#forml3").show();
        $("#p3").show();
    });

    $("#p3").click(function(){
    	
        $("#fl3").show();
        $("#p3").hide();
        $("#forml4").show();
        $("#p4").show();
    });

    $("#p4").click(function(){
    	
        $("#fl4").show();
        $("#p4").hide();
        $("#forml5").show();
        $("#p5").show();
    });

    $("#p5").click(function(){
    	
        $("#fl5").show();
        $("#p5").hide();
        $("#forml6").show();
        $("#p6").show();
    });

    $("#p6").click(function(){
    	
        $("#fl6").show();
        $("#p6").hide();
        $("#forml7").show();
        $("#p7").show();
    });

    $("#p7").click(function(){
    	
        $("#fl7").show();
        $("#p7").hide();
        $("#forml8").show();
        $("#p8").show();
    });

    $("#p8").click(function(){
    	
        $("#fl8").show();
        $("#p8").hide();
        $("#forml9").show();
        $("#p9").show();
    });

    $("#p9").click(function(){
    	
        $("#fl9").show();
        $("#p9").hide();
    });

});


$(function(){
    $("*.form_line").hide();
    $("*.fich_line").hide();
    $("#forml1").show();
    $("#fl1").show();
    $("#forml2").show();

    var checkf1 = $('#f1-clear_id').length;
    var checkf2 = $('#f2-clear_id').length;
    var checkf3 = $('#f3-clear_id').length;
    var checkf4 = $('#f4-clear_id').length;
    var checkf5 = $('#f5-clear_id').length;
    var checkf6 = $('#f6-clear_id').length;
    var checkf7 = $('#f7-clear_id').length;
    var checkf8 = $('#f8-clear_id').length;


    if(checkf1 > 0){
        $("#p2").click();
    };
    if(checkf2 > 0){
        $("#p3").click();
    };
    if(checkf3 > 0){
        $("#p4").click();
    };
    if(checkf4 > 0){
        $("#p5").click();
    };
    if(checkf5 > 0){
        $("#p6").click();
    };
    if(checkf6 > 0){
        $("#p7").click();
    };
    if(checkf7 > 0){
        $("#p8").click();
    };
    if(checkf8 > 0){
        $("#p9").click();
    };




});