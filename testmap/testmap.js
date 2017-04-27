function initMap() {
  var map = new google.maps.Map(document.getElementById('map_canvas'), {
    center: {lat: 32.2766,lng: -101.454},
    zoom: 6
  });

  var layer = new google.maps.FusionTablesLayer({
    query: {
      select: '\'Geocodable address\'',
      from: '1WaohAetRIdT4JIseylhSqxjWpnxQPm6SiREMjhx1'
    }
  });

  layer.setMap(map);
}
