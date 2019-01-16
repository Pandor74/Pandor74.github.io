
$(function(){
    
    $("*.p_detail").hide(0);


    //on init sur la présentation des agences
    $('#liste_container_personnes').hide(0);


    //Devellopement détails personnes
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


    //Affichage agences
    $('#Fagences').click(function(){
        $('#liste_container_entreprises').hide(0);
        $('#liste_container_agences').show(0);
        $('#liste_container_personnes').hide(0);
    });


    //Affichage personnes
    $('#Fpersonnes').click(function(){
        $('#liste_container_entreprises').hide(0);
        $('#liste_container_agences').hide(0);
        $('#liste_container_personnes').show(0);
    });
    


    });

//Attention ici tu as plusieurs liste donc tu ne peux pas te servir de la classe liste mais plutot des id en fonction de ce qui est caché ou pas
$(function(){
    var largeur=Math.round($("#liste_container_agences").width());
    lar=Math.trunc(largeur/400)*400;
    $(".liste").width(lar);


    });



//Resize ok
$(function(){
    $(window).resize(function(){
        var largeur=Math.round($(".liste_container").width());
       

        lar=Math.trunc(largeur/400)*400;
        $(".liste").width(lar);
    });

});