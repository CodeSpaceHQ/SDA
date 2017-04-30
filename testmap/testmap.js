function initMap() {
  var map = new google.maps.Map(document.getElementById('map_canvas'), {
    center: {lat: 32.2766,lng: -101.454},
    zoom: 6
  });

  var layer = new google.maps.FusionTablesLayer({
    query: {
      select: '\'Geocodable address\'',
      from: '10eIaqwKkNHAWeRvHMCGk18mTlrypPV7W7FpmVyC-'
    }
  });

  layer.setMap(map);
}
