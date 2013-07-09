

$(function() {
    var availStations = 
        ['red', 'blue', 'green', 'yellow', 'pink', 'black', 'purple'];
    
    $(".stations").autocomplete({
        source: availStations
    });
});

/*
$(function() {
    var availStations = 
        ['Chestnut H East',
         'Mt Airy',
         'Chestnut H West',
         'Allen Lane',
         'Stenton',
         'Bridesburg',
	 'Paoli',
	 'Jenkintown',
	 'Airport',
	 'Bristol',
	 'Wayne Junction',
	 'Germantown',
	 'Yardley',
	 'Bethayres',
	 'West Trenton',
	 'Somerton',
	 '30th Street Station'];
    
    $(".stations").autocomplete({
        source: availStations
    });
});
*/