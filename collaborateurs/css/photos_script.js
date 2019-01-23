

$(function(){

	//recalcule la dimension de la liste pour centrer les photos à l'ouverture
    var largeur=Math.round($(".liste_container").width());
    lar=Math.trunc(largeur/400)*400;
    
    $(".liste").width(lar);





	//recalcule la dimension de la liste pour centrer les photos en zoomant
    $(window).resize(function(){
        var largeur=Math.round($(".liste_container").width());
       

        lar=Math.trunc(largeur/400)*400;

        $(".liste").width(lar);
    });


    //GESTION DU PASSAGE EN PLEIN ECRAN AVEC FENETRE MODAL
    $("#all_photo_fullscreen").hide(0);

    $(".photo").on('click',function() {
		pleinEcran(this);

	});



	//gestion de l'appui sur echap pour fermer la visionneuse
    $(document).on('keyup',function(e){
      var key=e.which;

      if (key == 27) {
        
        $("#all_photo_fullscreen").hide(0);
        $('html, body').css({overflow: 'auto'});

      };


    });


    //gestion du click out sur zone grisé
    $("#all_photo_fullscreen").on('click',function(e){
      	
      	if ($(e.target).is("#Bprevious") | $(e.target).is("#Bnext") | $(e.target).is("#photo_wrapper") | $(e.target).is("#photo_player")) {
            return;
        }
        else {
            $("#all_photo_fullscreen").hide(0);
        	$('html, body').css({overflow: 'auto'});
        
        };
        
        

 


    });


});






function pleinEcran(element){


	$("#all_photo_fullscreen").show(0);;
    $('html, body').css({overflow: 'hidden'});

    var url = $(element).find("img").attr('src');
    $("#photo_player").attr('src',$(element).find("img").attr('src'));

    //créer une image virtuelle sans contrainte
    $("<img/>")
    	.attr("src",url)
    	.on("load",function (){
	    	var originalHeight = this.height;
	    	var originalWidth = this.width;

	    	if (originalWidth >= originalHeight) {
	    		$("#photo_player").css("width",'100%');
	    		$("#photo_player").css("height",'auto');
	    	}
	    	else {
	    		$("#photo_player").css("height",'100%');
	    		$("#photo_player").css("width",'auto');
	    	};

    });

    

};


