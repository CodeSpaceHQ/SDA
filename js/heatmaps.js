function initMap() {
  var map = new google.maps.Map(document.getElementById('map_canvas'), {
    center: {lat: 32.2766,lng: -101.454},
    zoom: 6
  });

  console.log('You fucker');
  var layer = new google.maps.FusionTablesLayer({
    query: {
      select: '\'Geocodable address\'',
      from: '1MW1A5r6QuM8SpApe9sa7ACV5mkodwuo3ry9-sutu'
    },
    styles: [{
      polygonOptions: {
        fillColor: '#274e13',
        fillOpacity: 1
      }
    }, {
      where: 'weight = 1',
      polygonOptions: {
        fillColor: '#d9ead3',
        fillOpacity: 1
      }
    }, {
      where: 'weight = 2',
      polygonOptions: {
        fillColor: '#b6d7a8',
        fillOpacity: 1
      }
    }, {
      where: 'weight = 3',
      polygonOptions: {
        fillColor: '#93c47d',
        fillOpacity: 1
      }
    }, {
      where: 'weight = 4',
      polygonOptions: {
        fillColor: '#6aa84f',
        fillOpacity: 1
      }
    }, {
      where: 'weight = 5',
      polygonOptions: {
        fillColor: '#38761d',
        fillOpacity: 1
      }
    }, {
      where: 'weight = 6',
      polygonOptions: {
        fillColor: '#274e13',
        fillOpacity: 1
      }
    }]
  });

  // testing choropleth layer
  var starbucks = new google.maps.FusionTablesLayer({
    query:{
      select: '\'Geocodable address\'',
      from: '1yCjcUA_wnMV5hDnj6aiS0eN0dS_3yvTiz-jvlVyB'
    }
  });

  layer.setMap(map);
  starbucks.setMap(map);
}
