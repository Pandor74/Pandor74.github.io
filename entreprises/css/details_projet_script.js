
$(function(){

    $("#b1").css('color','red');
    $(".projet_container_2").hide(0);


    $("#b1").on('click',
        function cache2montre1(){
            $("#b1").css('color','red');
            $("#b2").css('color','black');
            $(".projet_container_1").show(0);
            $(".projet_container_2").hide(0);
        }

      );
    
    $("#b2").on('click',
        function cache1montre2(){
            $("#b1").css('color','black');
            $("#b2").css('color','red');
            $(".projet_container_1").hide(0);
            $(".projet_container_2").show(0);
        }

      );


    function Redim(){
            

            if (($("#logo_projet").height() > 299) && ($("#logo_projet").height() < 301)) {

                var newWidth = $("#logo_projet").width() *2;
                var newHeight = $("#logo_projet").height() *2;
                
                $(this).animate({"width":Math.round(newWidth),"height":Math.round(newHeight),"origin":"left"},200);

                
           }
           else {
                var ratio =  $("#logo_projet").width() / $("#logo_projet").height();
                var newHeight = 300 ;
                var newWidth = newHeight * ratio;
                
                
                $(this).animate({"width":Math.round(newWidth),"height":Math.round(newHeight)},200);
                

           }

        };

    


    //pour redimensionner la photo logo on click
    $("#logo_projet").on('click',

        function checkAnim(){
            if (!$("#logo_projet").is(':animated')) {
                $("#logo_projet").click(Redim);
            }
           

        }
    );





    //pour la propsérité inutile actuellement
    $("#open_map1").on('click',callMap1);

    $("#close_map").on('click',closeMap);

});
//fin du call du DOM









    function callMap1(){
        $("#map1").width(450);
        $("#map1").height(300);

        var url="https://maps.googleapis.com/maps/api/js?key=AIzaSyA5GZhVtXpPmhluvhzToET_TXqAFB9hBZA&callback=initMap1"
        $.getScript(url);
        };

    function closeMap(){
      $("#map1").width(0);
      $("#map1").height(0);
    };



    function initMap1() {
      // The location of Uluru
      var loc = {lat: 45.777077, lng: 4.875454};
      // The map, centered at Uluru
      var map = new google.maps.Map(
          document.getElementById('map1'), {zoom: 14, center: loc});
      // The marker, positioned at Uluru
      var marker = new google.maps.Marker({position: loc, map: map});
    };


