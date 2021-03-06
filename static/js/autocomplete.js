// parents ajax request
function parentsAutocomplete(field){
		$.ajax( {
          url: "/parents/json",
          dataType: "json",
          success: function( data ) {
          	var options = {
          		data: data,
          		getValue: "name",
          		list: {
				        match: {
				            enabled: true
				        }
				    },
				    theme: "plate-dark"
          	};
            $(field).easyAutocomplete(options);
            console.log(options);
          }
        } );
}

// fathers ajax request
function fathersAutocomplete(field){
		$.ajax( {
          url: "/fathers/json",
          dataType: "json",
          success: function( data ) {
          	var options = {
          		data: data,
          		getValue: "name",
          		list: {
				        match: {
				            enabled: true
				        }
				    },
				    theme: "plate-dark"
          	};
            $(field).easyAutocomplete(options);
            console.log(options);
          }
        } );
}

//mothers ajax request
function mothersAutocomplete(field){
    $.ajax( {
          url: "/mothers/json",
          dataType: "json",
          success: function( data ) {
            var options = {
              data: data,
              getValue: "name",
              list: {
                match: {
                    enabled: true
                }
            },
            theme: "plate-dark"
            };
            $(field).easyAutocomplete(options);
          }
        } );
}


//students ajax request
function studentsAutocomplete(field){
    $.ajax( {
          url: "/students/json",
          dataType: "json",
          success: function( data ) {
            var options = {
              data: data,
              getValue: "name",
              list: {
                match: {
                    enabled: true
                }
            },
            theme: "plate-dark"
            };
            $(field).easyAutocomplete(options);
          }
        } );
}


//courses ajax request
function coursesAutocomplete(field){
    $.ajax( {
          url: "/courses/json",
          dataType: "json",
          success: function( data ) {
            var options = {
              data: data,
              getValue: "name",
              list: {
                match: {
                    enabled: true
                }
            },
            theme: "plate-dark"
            };
            $(field).easyAutocomplete(options);
          }
        } );

}


//locations ajax request
function locationsAutocomplete(field){
    $.ajax( {
          url: "/locations/json",
          dataType: "json",
          success: function( data ) {
            var options = {
              data: data,
              getValue: "name",
              list: {
                match: {
                    enabled: true
                }
            },
            theme: "plate-dark"
            };
            $(field).easyAutocomplete(options);
          }
        } );

}