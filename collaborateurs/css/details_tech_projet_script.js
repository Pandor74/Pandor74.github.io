
$(function(){

    $(".ligne_ratio").hide(0);
    $(".liste_tranches").hide(0);

    //dimensionnnement auto des tranches
    var nb_tranche = $(".liste_tranches:first").find(".tranche").length;

    

    $(".valeurs").each(function(){
      if ($(this).parent().css('display') != "none") {
        var largeur = $(this).width() / nb_tranche;
        $(".tranche").width(largeur);
        return false;
      };
    })
    
    



    //maj auto des valeurs identique en changement
    $(".ligne_ratio .valeurs input").on('keyup click',function update_auto(){
        var val = $(this).val();
        var nom_ratio_courant = $(this).parent().parent().prev(".nom_ratio").text();

        var num_tranche=$(this).parent().prevAll(".tranche").length;

        


        $(".nom_ratio").each(function cherche_same(){
            if (nom_ratio_courant == $(this).text()) {
                $(this).next(".valeurs").find(".tranche").eq(num_tranche).find("input").val(val);

            };



        });


    });


    //maj auto des valeurs identique en changement du nommage de tranche
    $(document).on('keyup','.liste_tranches .valeurs .tranche input',function update_nom(){
  
        var val = $(this).val();
 
        var num_tranche=$(this).parent().prevAll(".tranche").length;
        

        


        $(".liste_tranches").each(function cherche_same_nom(){
            
          $(this).find(".valeurs").find(".tranche").eq(num_tranche).find("input").val(val);

            



        });


    });



    //gestion du redimensionnement et maj des tailles de colonnes 
    $(window).on('resize',MAJ_taille);


    $(".plus").on("click",function(){
      $(this).parent().nextAll(".liste_tranches").toggle();
      $(this).parent().nextAll(".ligne_ratio").toggle();
      MAJ_taille();

    });


    //AJOUT DE TRANCHE

    //gestion de l'ajout de tranche

    $("#add_tranche").on('click',function (){
      $("#dialog_add").dialog("open");

    });


    //définition de la boite de dialog de suppression avec jquery UI
    $("#dialog_add").dialog({
      autoOpen : false,
      draggable:true,
      height:200,
      width:400,
      modal:true,
      buttons: [
        {
          text: "Ajouter",
          icon: "ui-icon-disk",
          click: function() {
            $( this ).dialog( "close" );
            var tranche_a_add = $("#in_add_tranche").val();
            Ajouter_Tranche(tranche_a_add);
          }
     
          // Uncommenting the following line would hide the text,
          // resulting in the label being used as a tooltip
          //showText: false
        },
        {
          text: "Annuler",
          icon: "ui-icon-arrowreturnthick-1-w",
          click: function() {
            $( this ).dialog( "close" );
          }
     
          // Uncommenting the following line would hide the text,
          // resulting in the label being used as a tooltip
          //showText: false
        },
      ]
    });


    //gestion de l'appui sur entrer dans la boite de dialog d'ajout
    $("#dialog_add #in_add_tranche").on('keyup',function(e){
      var key=e.which;

      if (key == 13) {
        //dupliquer la fonction de la boite de dialog
        $("#dialog_add").dialog( "close" );
        var tranche_a_add = $(this).val();
        Ajouter_Tranche(tranche_a_add);
      };


    });




    //SUPPRESSION DE TRANCHE

    //gestion de la suppresion de tranche
    $("#del_tranche").on('click',function (){
      var nb_tranche = $(".liste_tranches:first").find(".tranche").length;

      if (nb_tranche > 1) {
        $("#dialog_del").dialog("open");
      }
      else {
        alert("Il n'y a que la tranche principale ! Vous ne pouvez pas la supprimer")
      }

    });


    //définition de la boite de dialog de suppression avec jquery UI
    $("#dialog_del").dialog({
      autoOpen : false,
      draggable:true,
      height:200,
      width:400,
      modal:true,
      buttons: [
        {
          text: "Supprimer",
          icon: "ui-icon-trash",
          click: function() {
            $( this ).dialog( "close" );
            var tranche_a_del = $("#in_del_tranche").val();
            Supprimer_Tranche(tranche_a_del);
          }
     
          // Uncommenting the following line would hide the text,
          // resulting in the label being used as a tooltip
          //showText: false
        },
        {
          text: "Annuler",
          icon: "ui-icon-arrowreturnthick-1-w",
          click: function() {
            $( this ).dialog( "close" );
          }
     
          // Uncommenting the following line would hide the text,
          // resulting in the label being used as a tooltip
          //showText: false
        },
      ]
    });



    


});
//fin de l'event listener !
    


function MAJ_taille(){
  //dimensionnnement auto des tranches
  var nb_tranche = $(".liste_tranches:first").find(".tranche").length;

  $(".valeurs").each(function(){
    if ($(this).parent().css('display') != "none") {
      var largeur = $(this).width() / nb_tranche;
      $(".tranche").width(largeur);
      return false;
    };
  });

};


//fonction pour ajouter une tranche et ajuster la taille au passage
function Ajouter_Tranche(nom_tranche) {
  
  //ajout du nouveau div
  $("<div>",{
    class:"tranche",

  }).appendTo(".liste_tranches .valeurs");


  //ajout du nouveau input dans le div précédent
  var endroit = $(".liste_tranches .valeurs").find(".tranche:last")

  $("<input>",{
    val:nom_tranche.toUpperCase(),
  }).appendTo(endroit)


  //Ajout de l'option de suppresion dans la boite de suppression
  var nb_tranche = $(".liste_tranches:first").find(".tranche").length;
  $("<option>",{
    val:nb_tranche - 1,
    text:nom_tranche.toUpperCase(),

  }).appendTo("#dialog_del select")


  //copy de l'input de chaque ligne de ratio correspondant
  $(".ligne_ratio .valeurs").each(function ajoute_input(){
    $(this).find(".tranche:last").clone(true,true).appendTo(this);
  });



  MAJ_taille();

};



//fonction pour supprimer une tranche et ajuster la taille au passage
function Supprimer_Tranche(num_tranche) {
  
  var nb_tranche = $(".liste_tranches:first").find(".tranche").length;

  if (num_tranche != 0) {
    //suppresion de la tranche dans les listes
    $(".liste_tranches .valeurs").each(function (){

      $(this).find(".tranche").eq(num_tranche).remove();

    });


    
    //suppresion de l'option dans la boite de suppression
    var found=false;
    $("#dialog_del").find("select").find("option").each(function(){
      if (($(this).val() == num_tranche ) & (!found)) {
        $(this).remove()
        found=true;
      }
      else if (found) {
        //maj des valeurs suivantes pour recoller après la suppression 
        var new_val=$(this).val() - 1 ;
        $(this).val(new_val);
      };
    });


    //suppresion des des lignes de ratio correspondant
    $(".ligne_ratio .valeurs").each(function delete_input(){
      $(this).find(".tranche").eq(num_tranche).remove();
    });

    MAJ_taille();
  }
  else {
    alert("Vous ne pouvez pas supprimer la tranche totale !")
  };

};