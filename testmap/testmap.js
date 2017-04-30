function initMap() {
  var map = new google.maps.Map(document.getElementById('map_canvas'), {
    center: {lat: 32.2766,lng: -101.454},
    zoom: 6
  });

  var layer = new google.maps.FusionTablesLayer({
    query: {
      select: '\'Geocodable address\'',
      from: '10eIaqwKkNHAWeRvHMCGk18mTlrypPV7W7FpmVyC-'
    },
    heatmap: {
      enabled: true,
      valueField: 'AGI_STUB'
    }
  });

  // testing choropleth layer
  var choro_layer = new google.maps.Data();
  choro_layer.loadGeoJson('');

  choro_layer.setStyle(function(feature) {
    return {
      fillColor: '',
      fillOpacity: 0.8,
      strokeColor: '',
      strokeWeight: 1,
      zIndex: 1
    };
  });

  layer.setMap(map);
}
