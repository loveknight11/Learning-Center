var fathers = [];
var mothers = [];

// fathers ajax request
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
            $('#father').easyAutocomplete(options);
            console.log(options);
          }
        } );

//mothers ajax request
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
            $('#mother').easyAutocomplete(options);
            console.log(options);
          }
        } );