
$(function(){
    
    


    $("*.p_detail").hide(0);


	$(".plus").click(function(){
        
        $(this).parent().parent().next(".detail_ent").toggle("drop");
        

        var val = $(this).text();


        if (val == "+") {
        	$(this).text("-");
            $(this).parent().parent().css('border-bottom','2px solid black');
            $(this).parent().parent().parent().find('.antennes_ent').css('border-top','2px solid black');
        }
        else {
        	$(this).text("+");
            $(this).parent().parent().css('border','0px');
            $(this).parent().parent().parent().find('.antennes_ent').css('border-top','0px');
        };
    
        //gestion de la taille d ela liste des antennes de l'entreprise
        if ((this.id == "plus_agences") || (this.id == "plus_personnel")) {
            var largeur=Math.round($(".ent_wrapper").width());
            var lar_max=Math.trunc(largeur/400)*400;

            $(".liste").each(function(){
                var lar_item_ag=$(this).find(".agence").length * 400;
                var lar_item_per=$(this).find(".personne").length * 400;

                if (lar_item_ag > 0 ) {
                    $(this).width(Math.min(lar_max,lar_item_ag));
                }
                else {
                    $(this).width(Math.min(lar_max,lar_item_per));
                };


                
            });

            if (this.id == "plus_agences") {
                $("#wrapper_agences").find(".p_detail").hide(0);
            }
            else {
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
            $(this).parent().css('border-bottom','solid black 1px');
        }
        else {
            $(this).text("+");
            $(this).parent().css('border-bottom','solid black 0px');
        };

        
       
        
        });

    });



//Attention ici tu as plusieurs liste donc tu ne peux pas te servir de la classe liste mais plutot des id en fonction que qui est caché ou pas




//Resize ok
$(function(){
    $(window).resize(function(){
        var largeur=Math.round($(".ent_wrapper").width());
        lar_max=Math.trunc(largeur/400)*400;

        $(".liste").each(function(){
            var lar_item_ag=$(this).find(".agence").length * 400;
            var lar_item_per=$(this).find(".personne").length * 400;
            



            if (lar_item_ag > 0 ) {
                $(this).width(Math.min(lar_max,lar_item_ag));
                
            }
            else {
                
                $(this).width(Math.min(lar_max,lar_item_per));
               
            };

        });


    });

});


$(function(){
    var largeur=Math.round($(".ent_wrapper").width());
    var lar_max=Math.trunc(largeur/400)*400;

    $(".liste").each(function(){
        var lar_item_ag=$(this).find(".agence").length * 400;
        var lar_item_per=$(this).find(".personne").length * 400;

        if (lar_item_ag > 0 ) {
            $(this).width(Math.min(lar_max,lar_item_ag));
        }
        else {
            $(this).width(Math.min(lar_max,lar_item_per));
        };
    });
});