
$(function(){
    


    initialise_calendar();



    //passage à la semaine à 5 jours
    $('#F5j').on('click',semaine_normale);


    //passage à la semaine à 7 jours
    $('#F7j').on('click',semaine_complete);


    $('#Favant').on('click',prev_month);
    $('#Fapres').on('click',next_month);


});

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
        $(id_case).text('Janvier ' + annee.toString());
    }
    else if (mois == 2 ) {
        $(id_case).text('Février ' + annee.toString());
    }
    else if (mois == 3 ) {
        $(id_case).text('Mars ' + annee.toString());
    }
    else if (mois == 4 ) {
        $(id_case).text('Avril ' + annee.toString());
    }
    else if (mois == 5 ) {
        $(id_case).text('Mai ' + annee.toString());
    }
    else if (mois == 6 ) {
        $(id_case).text('Juin ' + annee.toString());
    }
    else if (mois == 7 ) {
        $(id_case).text('Juillet ' + annee.toString());
    }
    else if (mois == 8 ) {
        $(id_case).text('Août ' + annee.toString());
    }
    else if (mois == 9 ) {
        $(id_case).text('Septembre ' + annee.toString());
    }
    else if (mois == 10 ) {
        $(id_case).text('Octobre ' + annee.toString());
    }
    else if (mois == 11 ) {
        $(id_case).text('Novembre ' + annee.toString());
    }
    else if (mois == 12 ) {
        $(id_case).text('Décembre ' + annee.toString());
    } 
    else if (mois == 0 ) {
        $(id_case).text('Décembre ' + (annee-1).toString());
    } 
    else if (mois == 13 ) {
        $(id_case).text('Janvier ' + (annee+1).toString());
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

function displayFromDate(mois,annee){
    var d = new Date(annee,mois,1);

    var mois = d.getMonth()+1;
    var date = d.getDate();
    var jour = d.getDay();
    var annee=d.getFullYear();

    EcrisMois('#date_title',mois,annee);
    EcrisMois('#Favant',mois-1,annee);
    EcrisMois('#Fapres',mois+1,annee);


    var i;
    var j;
    var calc = date - jour;
    d.setDate(calc);

    

    $(".cal_week").each(function(){
        $(this).find(".cal_day").each(function(){
            d.setDate(d.getDate() + 1);
            if (d.getDate() == 1) {
                if ((d.getMonth()+1 ) == 1 ){
                    ecrire='0' + d.getDate().toString() +'/' + '0' + (d.getMonth()+1).toString() +'/' + d.getFullYear().toString();
                }
                else if ((d.getMonth()+1)<10) {
                    ecrire='0' + d.getDate().toString() +'/' + '0' + (d.getMonth()+1).toString();
                }
                else {
                    ecrire='0' + d.getDate().toString() +'/' + (d.getMonth()+1).toString();
                };
            }
            else if (d.getDate() < 10 ) {
                ecrire='0' + d.getDate().toString();
            }
            else {
                ecrire=d.getDate().toString();
            };

            $(this).find(".num_day").text(ecrire);
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
        var deb_mois = false;
        var test;

        $('.cal_week .cal_day').each(function(){
            if (!deb_mois) {
                var jour_test = $(this).find(".num_day").text();

                test = jour_test.split("/");
                

                if (test.length > 1) {
                    deb_mois=true;
                } ;
            }
            else {
                var jour_test = $(this).find(".num_day").text();

                test = jour_test.split("/");

                if (jour == test[0]) {
                    $(this).css('background-color','#910000');
                    $(this).css('color','white');

                    return false;

                };

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
        $(this).find(".cal_day").eq(5).css('background-color','rgba(20,20,20,0.75)');
        $(this).find(".cal_day").eq(6).css('background-color','rgba(20,20,20,0.75)');

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

    var tab = ReverseEcrisMois('#Favant');

    reinitCouleurs();

    displayFromDate(tab[0]-1,tab[1]);
    


};



function next_month () {
    var tab = ReverseEcrisMois('#Fapres');

    reinitCouleurs();
    displayFromDate(tab[0]-1,tab[1]);

};