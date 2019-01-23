
var grandi=false;
var element;

$(function(){
    


    initialise_calendar();

    //disable possibilité de changement de mois et tous si grandi
    
    //passage à la semaine à 5 jours
    $('#F5j').on('click',function(){
        if (!grandi) {
            semaine_normale();
        };
    });


    //passage à la semaine à 7 jours
    $('#F7j').on('click',function(){
        if (!grandi) {
            semaine_complete();
        };
    });

    //click sur bouton précédent
    $('#Favant').on('click',function(){
        if (!grandi) {
            prev_month();
        }
        else {
            prev_day();
        };
    });


    //click sur bouton suivant
    $('#Fapres').on('click',function(){
        if (!grandi) {
            next_month();
        }
        else {
            next_day();
        };

    });
    


    //enleve le grandissement si click à l'extérieur du cadre calendrier
    $(document).on('click',function(e){
        if (grandi) {
            if ($(e.target).is(".cal_wrapper *")) {
                return;
            }
            else {
                reduce_day();
            
            };
        };
    });

     //grandi le jour sélectionné
    $(".cal_week .cal_day").on('click',function (){
        if (!grandi) {
            element = this;

            var test_date = parseInt($(element).find(".ecrire_date").find('.num_day').text());
            var test_month = parseInt($(element).find(".ecrire_date").find('.mois_day').text().split("/")[1]);
            var test_year = parseInt($(element).find(".ecrire_date").find(".annee_day").text().split("/")[1]);

            var tab_current = ReverseEcrisMois($("#date_tile"));

            if ( ( test_month != tab_current[0] ) | ( test_year != tab_current[1] ) ) {
                reinitCouleurs();
                displayFromDate(test_month-1,test_year);

                chercherPosition(test_date,test_month,test_year);
            };

            grow_day();

        };
    });



    $(window).resize(function(){
        if (grandi) {
            resize_growned_day();
        };

    });


   

});


function next_day(){
    reduce_day();

    var index_day =$(element).index();
    var index_week =$(element).parent().index();

    var current_date = parseInt($(element).find(".ecrire_date").find(".num_day").text());
    var current_month = parseInt($(element).find(".ecrire_date").find('.mois_day').text().split("/")[1]);
    var current_year = parseInt($(element).find(".ecrire_date").find(".annee_day").text().split("/")[1]);


    if (index_day < 6) {
        element=$(element).next(".cal_day");

        var next_date = parseInt($(element).find(".ecrire_date").find('.num_day').text());
        var next_month = parseInt($(element).find(".ecrire_date").find('.mois_day').text().split("/")[1]);
        var next_year = parseInt($(element).find(".ecrire_date").find(".annee_day").text().split("/")[1]);

        var tab_current = ReverseEcrisMois($("#date_tile"));

        if ( ( next_month != tab_current[0] ) | ( next_year != tab_current[1] ) ) {
            displayFromDate(next_month-1,next_year);

            chercherPosition(next_date,next_month,next_year);
        }


    }
    else if ((index_day == 6) & (index_week < 5)) {
        element=$(element).parent().next(".cal_week").find(".cal_day").eq(0);

        var next_date = parseInt($(element).find(".ecrire_date").find('.num_day').text());
        var next_month = parseInt($(element).find(".ecrire_date").find('.mois_day').text().split("/")[1]);
        var next_year = parseInt($(element).find(".ecrire_date").find(".annee_day").text().split("/")[1]);

        var tab_current = ReverseEcrisMois($("#date_tile"));

        if ( ( next_month != tab_current[0] ) | ( next_year != tab_current[1] ) ) {
            displayFromDate(next_month-1,next_year);

            chercherPosition(next_date,next_month,next_year);
        }

    }
    else if ((index_day == 6) & (index_week == 5)) {

        var d = new Date(current_year,current_month-1,current_date);
        d.setDate(d.getDate() + 1)

        displayFromDate(d.getMonth(),d.getFullYear());

        chercherPosition(d.getDate(),d.getMonth()+1,d.getFullYear());

    };




    grow_day();

};


function prev_day(){
    reduce_day();

    var index_day =$(element).index();
    var index_week =$(element).parent().index();
    var current_date = parseInt($(element).find(".ecrire_date").find(".num_day").text());
    var current_month = parseInt($(element).find(".ecrire_date").find('.mois_day').text().split("/")[1]);
    var current_year = parseInt($(element).find(".ecrire_date").find(".annee_day").text().split("/")[1]);

    if (index_day > 0) {
        element=$(element).prev(".cal_day");

        var prev_date = parseInt($(element).find(".ecrire_date").find('.num_day').text());
        var prev_month = parseInt($(element).find(".ecrire_date").find('.mois_day').text().split("/")[1]);
        var prev_year = parseInt($(element).find(".ecrire_date").find(".annee_day").text().split("/")[1]);

        var tab_current = ReverseEcrisMois($("#date_tile"));

        if ( ( prev_month != tab_current[0] ) | ( prev_year != tab_current[1] ) ) {
            displayFromDate(prev_month-1,prev_year);

            chercherPosition(prev_date,prev_month,prev_year);
        }
    }
    else if ((index_day == 0) & (index_week > 0)) {
        element=$(element).parent().prev(".cal_week").find(".cal_day").eq(6);


        var prev_date = parseInt($(element).find(".ecrire_date").find('.num_day').text());
        var prev_month = parseInt($(element).find(".ecrire_date").find('.mois_day').text().split("/")[1]);
        var prev_year = parseInt($(element).find(".ecrire_date").find(".annee_day").text().split("/")[1]);

        var tab_current = ReverseEcrisMois($("#date_tile"));

        if ( ( prev_month != tab_current[0] ) | ( prev_year != tab_current[1] ) ) {
            displayFromDate(prev_month-1,prev_year);

            chercherPosition(prev_date,prev_month,prev_year);
        }
    }

    //dans le cas ou on recalcule tout le tableau il faudra retrouver la bonne position
    else if ((index_day == 0) & (index_week == 0)) {

            var d = new Date(current_year,current_month-1,current_date);

            d.setDate(d.getDate() - 1)

            displayFromDate(d.getMonth(),d.getFullYear());

            chercherPosition(d.getDate(),d.getMonth()+1,d.getFullYear());

    };




    grow_day();

};



function chercherPosition(date,mois,annee){

    var trouve = false;

    $(".cal_week").each(function() {
        $(this).find(".cal_day").each(function(){
            var test_date = parseInt($(this).find(".ecrire_date").find(".num_day").text());
            var test_mois = parseInt($(this).find(".ecrire_date").find('.mois_day').text().split("/")[1]);
            var test_annee= parseInt($(this).find(".ecrire_date").find(".annee_day").text().split("/")[1]);

            if ((test_date == date) & (test_mois == mois) & (test_annee == annee)) {
                element=this;
                trouve=true;
                return false;
            };
        });

        if (trouve) {
            return false;
        };
    });
}



function grow_day(){
    
    grandi=true;
    var pos = $(".cal_weeks_wrapper").position();
    var largeur = $(".cal_weeks_wrapper").width();
    var hauteur = $(".cal_weeks_wrapper").height()
    $(element).css('position','absolute');
    $(element).css('top',pos.top - 50);
    $(element).css('left',pos.left);
    $(element).css('z-index','2');
    $(element).css('height',hauteur+50);
    $(element).css('width',largeur);
    $(element).css('border-bottom-right-radius',"25px");
    $(element).css('border-bottom-left-radius',"25px");
    $(element).find(".ecrire_date").find(".jour_day").css("display","block");

    $("#Favant").text("Précédent");
    $("#Fapres").text("Suivant");


};


function reduce_day(){

    var index_day =$(element).index();
    var index_week =$(element).parent().index();
    
    grandi=false;
    var pos = $(".cal_weeks_wrapper").position();
    var largeur = $(".cal_weeks_wrapper").width();
    var hauteur = $(".cal_weeks_wrapper").height()
    $(element).css('position','static');
    $(element).css('z-index','0');
    $(element).css('height','100%');
    $(element).css('width','100%');
    $(element).css('border-bottom-right-radius',"0px");
    $(element).css('border-bottom-left-radius',"0px");

    if (index_week == 5) {
        if (index_day == 0) {
            $(element).css('border-bottom-left-radius',"25px");
        }
        else if (index_day == 6) {
            $(element).css('border-bottom-right-radius',"25px");
        };
    };





    $(element).find(".ecrire_date").find(".jour_day").css("display","none");


    var tab = ReverseEcrisMois('#date_title');

    EcrisMois('#Favant',tab[0]-1,tab[1]);
    EcrisMois('#Fapres',tab[0]+1,tab[1]);

};


function resize_growned_day(){
    var pos = $(".cal_weeks_wrapper").position();
    var largeur = $(".cal_weeks_wrapper").width();
    var hauteur = $(".cal_weeks_wrapper").height()
    $(element).css('top',pos.top - 50);
    $(element).css('left',pos.left);
    $(element).css('height',hauteur+50);
    $(element).css('width',largeur);

    

};


function semaine_normale (){
        $(".cal_title").find(".cal_day").eq(5).hide(0);
        $(".cal_title").find(".cal_day").eq(6).hide(0);

        $(".cal_week").each(function(){
            $(this).find(".cal_day").eq(5).hide(0);
            $(this).find(".cal_day").eq(6).hide(0);
        });

        //gestion des intermédiaires
        $(".cal_week").each(function(){
            $(this).find(".cal_day").eq(4).css('box-shadow','inset -2px 0 10px 2px rgba(0, 0, 0, 1)');
        });

        //gestion du coin bas droite
        $(".cal_week").eq(5).find(".cal_day").eq(4).css('border-bottom-right-radius','25px');
        $(".cal_week").eq(5).find(".cal_day").eq(4).css('box-shadow','inset 0 -2px 10px 2px rgba(0, 0, 0, 1),inset -2px 0 10px 2px rgba(0, 0, 0, 1)');

        //gestion du dernier jour de la semaine
        $(".cal_title").find(".cal_day").eq(4).css('box-shadow','inset -2px 0 10px 2px rgba(0, 0, 0, 1)');
};


function semaine_complete (){
        $(".cal_title").find(".cal_day").eq(5).show(0);
        $(".cal_title").find(".cal_day").eq(6).show(0);

        $(".cal_week").each(function(){
            $(this).find(".cal_day").eq(5).show(0);
            $(this).find(".cal_day").eq(6).show(0);
        });

        //gestion des intermédiaires
        $(".cal_week").each(function(){
            $(this).find(".cal_day").eq(4).css('box-shadow','inset 0 0 10px 2px rgba(0, 0, 0, 1)');
        });

        //gestion du coin bas droite
        $(".cal_week").eq(5).find(".cal_day").eq(4).css('border-bottom-right-radius','0px');
        $(".cal_week").eq(5).find(".cal_day").eq(4).css('box-shadow','inset 0px -2px 10px 3px rgba(0, 0, 0, 1)');

        //gestion du dernier jour de la semaine
        $(".cal_title").find(".cal_day").eq(4).css('box-shadow','inset 0 0 10px 2px rgba(0, 0, 0, 1)');
};


//on initilise le calendrier en supposant qu'on s'en fou du passé donc la première ligne contient le jour d'aujourd'hui
function initialise_calendar(){
    var d = new Date();
    var jour = d.getDay();
    var mois = d.getMonth();
    var annee = d.getFullYear();

    displayFromDate(mois,annee);
    
}; 


//ecriture du mois en fonction de la date actuelle, gère passage année antérieure ou supérieure
function EcrisMois(id_case,mois,annee){

    if (mois == 1 ) {
        $(id_case).text('Janvier ' + parseInt(annee).toString());
    }
    else if (mois == 2 ) {
        $(id_case).text('Février ' + parseInt(annee).toString());
    }
    else if (mois == 3 ) {
        $(id_case).text('Mars ' + parseInt(annee).toString());
    }
    else if (mois == 4 ) {
        $(id_case).text('Avril ' + parseInt(annee).toString());
    }
    else if (mois == 5 ) {
        $(id_case).text('Mai ' + parseInt(annee).toString());
    }
    else if (mois == 6 ) {
        $(id_case).text('Juin ' + parseInt(annee).toString());
    }
    else if (mois == 7 ) {
        $(id_case).text('Juillet ' + parseInt(annee).toString());
    }
    else if (mois == 8 ) {
        $(id_case).text('Août ' + parseInt(annee).toString());
    }
    else if (mois == 9 ) {
        $(id_case).text('Septembre ' + parseInt(annee).toString());
    }
    else if (mois == 10 ) {
        $(id_case).text('Octobre ' + parseInt(annee).toString());
    }
    else if (mois == 11 ) {
        $(id_case).text('Novembre ' + parseInt(annee).toString());
    }
    else if (mois == 12 ) {
        $(id_case).text('Décembre ' + parseInt(annee).toString());
    } 
    else if (mois == 0 ) {
        $(id_case).text('Décembre ' + (parseInt(annee) - 1 ).toString());
    } 
    else if (mois == 13 ) {
        $(id_case).text('Janvier ' + (parseInt(annee) + 1).toString());
    };
    
};

//ressort le mois humain et l'année de la date inscrite dans la case
function ReverseEcrisMois(id_case){
    var chaine = $(id_case).text();
    var tab = chaine.split(" ");
    var mois = tab[0];
    var annee = tab[1]

    if (mois == "Janvier") {
        tab[0] = 1;
    }
    else if (mois == "Février") {
        tab[0] = 2;
    }
    else if (mois == "Mars") {
        tab[0] = 3;
    }
    else if (mois == "Avril") {
        tab[0] = 4;
    }
    else if (mois == "Mai") {
        tab[0] = 5;
    }
    else if (mois == "Juin") {
        tab[0] = 6;
    }
    else if (mois == "Juillet") {
        tab[0] = 7;
    }
    else if (mois == "Août") {
        tab[0] = 8;
    }
    else if (mois == "Septembre") {
        tab[0] = 9;
    }
    else if (mois == "Octobre") {
        tab[0] = 10;
    }
    else if (mois == "Novembre") {
        tab[0] = 11;
    }
    else if (mois == "Décembre") {
        tab[0] = 12;
    };


    return tab

};


//retourne le jour ecris pour un humain a poartir du numéro de 0 à 6
function EcrisJour(num){

    if (num == 1 ) {
        return "Lundi";
    }
    else if (num == 2 ) {
        return "Mardi";
    }
    else if (num == 3 ) {
        return "Mercredi";
    }
    else if (num == 4 ) {
        return "Jeudi";
    }
    else if (num == 5 ) {
        return "Vendredi";
    }
    else if (num == 6 ) {
        return "Samedi";
    }
    else if (num == 0 ) {
        return "Dimanche";
    };
    
};


// a besoin d'une entrée de mois de type informatique démarre a 0
function displayFromDate(mois,annee){
    var d = new Date(annee,mois,1);

    var mois = d.getMonth()+1;
    var date = d.getDate();
    var jour = d.getDay();
    var annee=d.getFullYear();

    var ecrire_jour;
    var ecrire_num;
    var ecrire_mois;
    var ecrire_annee

    EcrisMois('#date_title',mois,annee);
    EcrisMois('#Favant',mois-1,annee);
    EcrisMois('#Fapres',mois+1,annee);


    var i;
    var j;
    var calc = date - jour;
    d.setDate(calc);

    
    //ecriture du numéro de la date
    $(".cal_week").each(function(){
        $(this).find(".cal_day").each(function(){
            d.setDate(d.getDate() + 1);
            //si premier jour d'un mois
            if (d.getDate() == 1) {
                ecrire_num ='0' + d.getDate().toString();
                ecrire_annee ='/' + d.getFullYear().toString();
                //si premier jour d'une année
                if ((d.getMonth()+1 ) == 1 ){
                    ecrire_mois ='/' + '0' + (d.getMonth()+1).toString();
                    $(this).find(".mois_day").css('display','block');
                    $(this).find(".annee_day").css('display','block');
                }
                else if ((d.getMonth()+1)<10) {
                    ecrire_mois ='/' + '0' + (d.getMonth()+1).toString();
                    $(this).find(".mois_day").css('display','block');
                    $(this).find(".annee_day").css('display','none');
                }
                else {
                    ecrire_mois ='/' + (d.getMonth()+1).toString();
                    $(this).find(".mois_day").css('display','block');
                    $(this).find(".annee_day").css('display','none');
                    
                };
            }
            else if (d.getDate() < 10 ) {
                ecrire_num ='0' + d.getDate().toString();
                ecrire_annee ='/' + d.getFullYear().toString();

                if ((d.getMonth()+1)<10) {
                    ecrire_mois ='/' + '0' + (d.getMonth()+1).toString();
                    $(this).find(".mois_day").css('display','none');
                    $(this).find(".annee_day").css('display','none');
                }
                else {
                    ecrire_mois ='/' + (d.getMonth()+1).toString();
                    $(this).find(".mois_day").css('display','none');
                    $(this).find(".annee_day").css('display','none');
                    
                };
                
            }
            else {
                ecrire_num = d.getDate().toString();
                ecrire_annee ='/' + d.getFullYear().toString();
                if ((d.getMonth()+1)<10) {
                    ecrire_mois ='/' + '0' + (d.getMonth()+1).toString();
                    $(this).find(".mois_day").css('display','none');
                    $(this).find(".annee_day").css('display','none');
                }
                else {
                    ecrire_mois ='/' + (d.getMonth()+1).toString();
                    $(this).find(".mois_day").css('display','none');
                    $(this).find(".annee_day").css('display','none');
                    
                };
            };


            //calcul du jour à écrire
            ecrire_jour = EcrisJour(d.getDay());
            $(this).find(".ecrire_date").find(".jour_day").text(ecrire_jour);
            $(this).find(".jour_day").css('display','none');

            //ecriture des autres précalculés ci-dessus
            $(this).find(".ecrire_date").find(".num_day").text(ecrire_num);
            $(this).find(".ecrire_date").find(".mois_day").text(ecrire_mois);
            $(this).find(".ecrire_date").find(".annee_day").text(ecrire_annee);
        });
    });



    coloreToday();

};


function coloreToday() {
    var today = new Date()
    var mois = today.getMonth() + 1;
    var year = today.getFullYear();
    var jour = today.getDate();

    var tab = ReverseEcrisMois('#date_title');
   

    if ((mois == tab[0]) & (year == tab[1])) {

        var test_date;
        var test_mois;

        $('.cal_week .cal_day').each(function(){
            
            test_date = parseInt($(this).find(".ecrire_date").find(".num_day").text());
            test_mois = parseInt($(this).find(".ecrire_date").find(".mois_day").text().split("/")[1]);

            if ((test_date == jour) & (test_mois == mois)) {

                $(this).css('background-color','#910000');
                $(this).css('color','white');

                return false;

            };


                    


        });


    };

};


function reinitCouleurs() {
    $(".cal_week").each(function(){
        $(this).find(".cal_day").eq(0).css('background-color','white');
        $(this).find(".cal_day").eq(1).css('background-color','white');
        $(this).find(".cal_day").eq(2).css('background-color','white');
        $(this).find(".cal_day").eq(3).css('background-color','white');
        $(this).find(".cal_day").eq(4).css('background-color','white');
        $(this).find(".cal_day").eq(5).css('background-color','rgba(79,79,79,1)');
        $(this).find(".cal_day").eq(6).css('background-color','rgba(79,79,79,1)');

        $(this).find(".cal_day").eq(0).css('color','black');
        $(this).find(".cal_day").eq(1).css('color','black');
        $(this).find(".cal_day").eq(2).css('color','black');
        $(this).find(".cal_day").eq(3).css('color','black');
        $(this).find(".cal_day").eq(4).css('color','black');
        $(this).find(".cal_day").eq(5).css('color','white');
        $(this).find(".cal_day").eq(6).css('color','white');

    });
};


function prev_month () {

    var tab = ReverseEcrisMois('#date_title');

    reinitCouleurs();

    displayFromDate(tab[0]-2,tab[1]);
    


};



function next_month () {
    var tab = ReverseEcrisMois('#date_title');

    reinitCouleurs();
    displayFromDate(tab[0],tab[1]);

};