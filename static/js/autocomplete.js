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