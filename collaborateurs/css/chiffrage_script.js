
$(function(){
    
    $("*.ligne_descro").hide(0);


    //devellopement des lignes de description en click sur le plus de droite
	$(".plus").click(function(){
        
        $(this).parent().next(".ligne_descro").toggle();

        var val = $(this).text();
       
        if (this.id != "plus_global" ) {
            if (val == "+") {
            	$(this).text("-");
                $(this).parent().next(".ligne_descro").css('border-bottom','solid black 2px');
                $(this).parent().css("border-bottom","solid black 1px");
            }
            else {
            	$(this).text("+");
                $(this).parent().next(".ligne_descro").css('border-bottom','0px');
                $(this).parent().css("border-bottom","solid black 2px");
            };
        }
        else {
            
            if (val == "+") {
                $(this).text("-");
                $("*.ligne").show(0);
                
            }
            else {
                $(this).text("+");
                $("*.ligne").not("#ligne_titre").hide(0);
                $("*.ligne_descro").hide(0);
            };

        };

        
    });


    //mise a jour du prix total de la ligne quand on tape des valeurs dans le input du prix unitaire
    $(".poste_PU input").keyup(function(){
        var PU = $(this).val();
        var quant = $(this).parent().parent().find(".poste_quantite").text().replace(",",".");
        var total = PU * quant;

        var totalFR = total.toFixed(2).replace(".",",");
        
        if (quant != 0) {
            $(this).parent().parent().find(".poste_montant_HT").text(totalFR);
        };


        var racine_init = $(this).parent().parent().find(".num").text();
        var racine=racine_init.split(".");
        racine.pop();
        racine=racine.join(".");
        
        var long=racine.length;

        var somme = 0;
        $(".num").each(function(){
            var racine_test = $(this).text().substring(0,long);
            if (racine_test == racine) {
                if ($(this).parent().parent().find(".poste_montant_HT").text() != "") {
                    somme += parseFloat($(this).parent().parent().find(".poste_montant_HT").text().replace(",","."));
                };
            };
        });
        
        var sommeFR = somme.toFixed(2).replace(".",",");
        
        $(this).closest(".ligne").nextAll(".ligne_ST:first").find(".poste_montant_HT").text(sommeFR);
        
    });








    //devellopement des sous poste lors du click de gauche
    $(".dev").click(function(){
        var val = $(this).text();
        var racine = $(this).parent().find('.num').text();
        var long = racine.length;

        if (val == "+") {
            $(this).text('-');
            $('.dev').not(this).each(function(){
                var num_poste_test = $(this).parent().find('.num').text()
                var racine_test = num_poste_test.substring(0,long);

                if (racine == racine_test) {
                    $(this).parent().parent().show(0);
                    $(this).closest(".ligne").nextAll(".ligne_ST:first").show(0);
                };



            });
        }
        else {
            $(this).text('+');
            $('.dev').not(this).each(function(){
                var num_poste_test = $(this).parent().find('.num').text()
                var racine_test = num_poste_test.substring(0,long);

                if (racine == racine_test) {
                    $(this).parent().parent().hide(0);
                    $(this).closest(".ligne").nextAll(".ligne_ST:first").hide(0);
                    if ($(this).parent().parent().next(".ligne_descro").css('display') != "none") {
                        $(this).parent().parent().find(".plus").click();
                    };
                };

            });
        };


    });


});




//Ce qui ce passe dès l'ouverture du template
$(function (){
    var lar_num = $("#num").innerWidth();
    var lar_des = $("#des").innerWidth();
    var lar_unite = $("#unite").innerWidth();
    var lar_quantite = $("#quantite").innerWidth();
    var lar_PU = $("#PU").innerWidth();
    var lar_montant_HT = $("#montant_HT").innerWidth();

    $(".poste_num").innerWidth(lar_num);
    $(".poste_des").innerWidth(lar_des);
    $(".poste_unite").innerWidth(lar_unite);
    $(".poste_quantite").innerWidth(lar_quantite);
    $(".poste_PU").innerWidth(lar_PU);
    $(".ligne .poste_montant_HT").innerWidth(lar_montant_HT);
    $(".ligne_ST .poste_montant_HT").innerWidth(lar_montant_HT + 32);

    $(window).resize(function(){
        var lar_num = $("#num").innerWidth();
        var lar_des = $("#des").innerWidth();
        var lar_unite = $("#unite").innerWidth();
        var lar_quantite = $("#quantite").innerWidth();
        var lar_PU = $("#PU").innerWidth();
        var lar_montant_HT = $("#montant_HT").innerWidth();

        $(".poste_num").innerWidth(lar_num);
        $(".poste_des").innerWidth(lar_des);
        $(".poste_unite").innerWidth(lar_unite);
        $(".poste_quantite").innerWidth(lar_quantite);
        $(".poste_PU").innerWidth(lar_PU);
        $(".ligne .poste_montant_HT").innerWidth(lar_montant_HT);
        $(".ligne_ST .poste_montant_HT").innerWidth(lar_montant_HT + 32);

        //on recommence si il n'a pas eu el temps de faire les modifs correctement
        if ($(".poste_num").innerWidth().toFixed(2) != lar_num.toFixed(2)) {
            var lar_num = $("#num").innerWidth();
            var lar_des = $("#des").innerWidth();
            var lar_unite = $("#unite").innerWidth();
            var lar_quantite = $("#quantite").innerWidth();
            var lar_PU = $("#PU").innerWidth();
            var lar_montant_HT = $("#montant_HT").innerWidth();

            $(".poste_num").innerWidth(lar_num);
            $(".poste_des").innerWidth(lar_des);
            $(".poste_unite").innerWidth(lar_unite);
            $(".poste_quantite").innerWidth(lar_quantite);
            $(".poste_PU").innerWidth(lar_PU);
            $(".ligne .poste_montant_HT").innerWidth(lar_montant_HT);
            $(".ligne_ST .poste_montant_HT").innerWidth(lar_montant_HT + 32);
        };
    });
});