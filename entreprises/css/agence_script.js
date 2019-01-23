
$(function(){
    
    $("#detail_personnel").hide(0);


    $("*.p_detail").hide(0);


	$(".plus").click(function(){
        
        $(this).parent().parent().next(".detail_age").toggle("drop");

        var val = $(this).text();


        if (val == "+") {
        	$(this).text("-");
        }
        else {
        	$(this).text("+");
        };
    
        //gestion de la taille de la liste des antennes de l'entreprise
        if ((this.id == "plus_personnel")) {
            var largeur=Math.round($(".age_wrapper").width());
            lar_max=Math.trunc(largeur/400)*400;

            $(".liste").each(function(){
                
                var lar_item_per=$(this).find(".personne").length * 400;

                if (lar_item_per > 0 ) {
                    $(this).width(Math.min(lar_max,lar_item_per));
                };


                
            });

            if (this.id == "plus_personnel") {
                $("#wrapper_personnel").find(".p_detail").hide(0);
            };


        };
        
        $([document.documentElement, document.body]).animate({
            scrollTop: $(this).offset().top
            }, 1000
        );

    });


    $(".bouton").click(function(){
        
        $(this).parent().next(".p_detail").toggle("drop");

        var val = $(this).text();


        if (val == "+") {
            $(this).text("-");
        }
        else {
            $(this).text("+");
        };

        
       
        
        });

    });



//Attention ici tu as plusieurs liste donc tu ne peux pas te servir de la classe liste mais plutot des id en fonction que qui est caché ou pas




//Resize ok
$(function(){
    $(window).resize(function(){
        var largeur=Math.round($(".age_wrapper").width());
        lar_max=Math.trunc(largeur/400)*400;

        $(".liste").each(function(){
            var lar_item_per=$(this).find(".personne").length * 400;
            



            if (lar_item_per > 0 ) {
                
                $(this).width(Math.min(lar_max,lar_item_per));
               
            };

        });


    });

});