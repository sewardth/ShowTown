//Google Maps GeoCode API

$(document).ready(function(){
  $("#zip").change(function(){
  	var zip = $('#zip').val();
    $.get("http://maps.googleapis.com/maps/api/geocode/json?address="+zip,function(data,status){
      var results = data.results[0];

      //builds object with address types
      address_types ={}
      for (x in results.address_components)
      {
      	address_types[results.address_components[x]['types'][0]] = {'short_name': results.address_components[x]['short_name'], 'long_name':results.address_components[x]['long_name']};
      }
      
      //test if zip is valid US code
      if (address_types.country.short_name !== 'US')
      {
      	//display error and disable form
      	$('#error_output').html('Not a valid Zip Code');
	  	$("input[type=submit]").attr("disabled", "disabled");


	  }

	  else
	  {
	  	//populate form fields
	      $('#error_output').html('');
	      $("input[type=submit]").removeAttr("disabled"); 
	      $('#state').val(address_types.administrative_area_level_1.long_name);
	      $('#city').val(address_types.locality.long_name);
	      $('#latitude').val(results.geometry.location.lat);
	      $('#longitude').val(results.geometry.location.lng);
        $('#country').val(address_types.country.short_name);
	  }



    });
  });
});