
$(function(){
    
    
    $("#inside_CCTP").hide(0);


    //Affichage du block pdf CCTP par le bouton en haut
    $("#CCTP_new_onglet").on('click',function(){
        window.open("../media/test.pdf")

    });



    //Affichage du block pdf CCTP par le bouton en haut
    $("#CCTP_inside").on('click',function(){
        $("#inside_CCTP").toggle(0);

    });

    //fermeture du block pdf CCTP par le bouton fermer
    $("#Bfermer").on('click',function(){
        $("#inside_CCTP").hide(0);

    });

    //empêche le drag si début de click sur le bouton
    $("#Bfermer").on('mousedown',function(e){
        e.stopPropagation();
    });

    //Augmentation de la hauteur du block PDF
    $("#Bplus").on('click',function(){
        var hauteur = $("#inside_CCTP").height();
        var ratio = hauteur / $(window).height();
        
        ratio = (ratio + 0.05)*100;
        var new_hauteur = ratio + 'vh';
        $("#inside_CCTP").css('height',new_hauteur);

    });

    //empêche le drag si début de click sur le bouton
    $("#Bplus").on('mousedown',function(e){
        e.stopPropagation();
    });

    //Diminution de la hauteur du block PDF
    $("#Bmoins").on('click',function(){
        var hauteur = $("#inside_CCTP").height();
        var ratio = hauteur / $(window).height();
        
        ratio = (ratio - 0.05)*100;
        var new_hauteur = ratio + 'vh';
        $("#inside_CCTP").css('height',new_hauteur);

    });

    //empêche le drag si début de click sur le bouton
    $("#Bmoins").on('mousedown',function(e){
        e.stopPropagation();
    });


    //essai de drag and drop width
    var isDragging=false;
    var iniY = 0;
    var finalY = 0;
    $(".CCTP_supp")
    .mousedown(function(event) {

        isDragging = true;
        iniY=event.clientY;
    });

    $(document).mousemove(function(event) {
        finalY=event.clientY;
        delta=finalY-iniY;
        if (((delta > 10 ) | (delta < - 10)) & (isDragging)){
            var hauteur = $("#inside_CCTP").height();
            var ratio = (hauteur - delta ) / $(window).height();
            
            ratio = ratio * 100;
            var new_hauteur = ratio + 'vh';
            $("#inside_CCTP").css('height',new_hauteur);
            iniY = event.clientY;
         };
    });



    $(document).mouseup(function(){
        isDragging = false;
        iniY=0;
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
    $(".ligne_ST .poste_montant_HT").innerWidth(lar_montant_HT);

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
        $(".ligne_ST .poste_montant_HT").innerWidth(lar_montant_HT);

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
            $(".ligne_ST .poste_montant_HT").innerWidth(lar_montant_HT);
        };
    });
});