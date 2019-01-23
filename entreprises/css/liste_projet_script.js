
$(function(){
    var largeur=Math.round($(".liste_container").width());

    lar=Math.trunc(largeur/400)*400;
    
    $(".liste").width(lar);


    });


$(function(){
    $(window).resize(function(){
        var largeur=Math.round($(".liste_container").width());
       

        lar=Math.trunc(largeur/400)*400;

        $(".liste").width(lar);
    });

});