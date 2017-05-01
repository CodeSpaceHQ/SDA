function initMap() {
  var map = new google.maps.Map(document.getElementById('map_canvas'), {
    center: {lat: 32.2766,lng: -101.454},
    zoom: 6
  });

  var layer = new google.maps.FusionTablesLayer({
    query: {
      select: '\'Geocodable address\'',
      from: '10eIaqwKkNHAWeRvHMCGk18mTlrypPV7W7FpmVyC-',
      where: 'TOTAL_INCOME > 0 AND STATE = \'TX\'',
      styles : [{
          polygonOptions: {
            fillColor: '#3E2723', // brown
            fillOpacity: 1
          }
        },
        {
          where: 'AGI_STUB = 6',
          polygonOptions: {
            fillColor: '#00BCD4',
            fillOpacity: 1
          }
        }
      ]
    }
  });

  // testing choropleth layer
  var starbucks = new google.maps.FusionTablesLayer({
    query:{
      select: '\'Geocodable address\'',
      from: '1yCjcUA_wnMV5hDnj6aiS0eN0dS_3yvTiz-jvlVyB',
      where: 'STATE = \'TX\''
    }
  });

  layer.setMap(map);
  starbucks.setMap(map);
}
