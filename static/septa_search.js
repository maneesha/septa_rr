/*
Would like to get complete station list from SEPTA.
Station names in SEPTA's GTFS dataset are not exact matches for how station names appear in trainview. 
*/

//List of stations to populate pull down menu in search form.
//Right now it's just a random sampling to ensure functionality of autocomplete in pull-down menu.

$(function() {
    var availStations = [

    'Airport',
    'Allen Lane',
    'Bethayres',
    'Bridesburg',
    'Bristol',
    'Chestnut H East',
    'Chestnut H West',
    'Germantown',
    'Jenkintown',
    'Paoli',
    'Somerton',
    'Stenton',
    'Trenton',
    'West Trenton',
    'Yardley'
    ];
    
    $(".stations").autocomplete({
        source: availStations
    });

});



  $(function() {
    $( ".datepicker" ).datepicker({minDate: new Date(2013, 4-1, 01), maxDate: '0'});
  });