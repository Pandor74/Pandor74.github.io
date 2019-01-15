
$(function(){

    $(".ligne_ratio").hide(0);

    //dimensionnnement auto des tranches
    var nb_tranche = $("#liste_tranches").find(".tranche").length;

    $(".valeurs").each(function(){
      if ($(this).parent().css('display') != "none") {
        var largeur = $(this).width() / nb_tranche;
        $(".tranche").width(largeur);
        return false;
      };
    })
    
    



    //maj auto des valeurs identique en changement
    $(".valeurs input").on('keyup click',function update_auto(){
        var val = $(this).val();
        var nom_ratio_courant = $(this).parent().parent().prev(".nom_ratio").text();

        var num_tranche=$(this).parent().prevAll(".tranche").length;

        


        $(".nom_ratio").each(function cherche_same(){
            if (nom_ratio_courant == $(this).text()) {
                $(this).next(".valeurs").find(".tranche").eq(num_tranche).find("input").val(val);

            };



        });


    });


    //gestion du redimensionnement et maj des tailles de colonnes 
    $(window).on('resize',MAJ_taille);


    $(".plus").on("click",function(){
      $(this).parent().nextAll(".ligne_ratio").toggle();
      MAJ_taille();

    });





});
    


function MAJ_taille(){
      //dimensionnnement auto des tranches
      var nb_tranche = $("#liste_tranches").find(".tranche").length;

      $(".valeurs").each(function(){
        if ($(this).parent().css('display') != "none") {
          var largeur = $(this).width() / nb_tranche;
          $(".tranche").width(largeur);
          return false;
        };
      })

    };