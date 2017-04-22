Plotly.d3.csv('https://raw.githubusercontent.com/CodeSpaceHQ/SDA/master/datasets/starbucks.csv', function(err, rows) {
    function unpack(rows, key) {
        return rows.map(function(row) {
            return row[key];
        });
    }

    var data = [{
        type: 'scattergeo',
        locationmode: 'USA-states',
        lon: unpack(rows, 'LONG'),
        lat: unpack(rows, 'LAT'),
        mode: 'markers',
        text: unpack(rows, 'CITY'),
        marker: {
            size: 2,
            opacity: 0.8,
            reversescale: true,
            autocolorscale: false,
            symbol: 'circle',
            line: {
                width: 1,
                color: 'rgb(102,102,102)'
            },
            cmin: 0,
            color: 'rgb(79,55,48)',
        }
    }];


    var layout = {
        title: 'StarBuck Locations in the US',
        geo: {
            scope: 'usa',
            projection: {
                type: 'albers usa'
            },
            showland: true,
            landcolor: 'rgb(250,250,250)',
            subunitcolor: 'rgb(217,217,217)',
            countrycolor: 'rgb(217,217,217)',
            countrywidth: 0.5,
            subunitwidth: 0.5
        }
    };

    Plotly.plot(myDiv, data, layout, {
        showLink: false
    });

});


Plotly.d3.csv('https://raw.githubusercontent.com/CodeSpaceHQ/SDA/master/datasets/income-data.csv', function(errors, rows) {
  function unpack(rows, key) {
      return rows.map(function(row) {
          return row[key];
      });
  }

  var data = [{
    type: 'choropleth',
    location: unpack(rows, 'ZIPCODE'),
    z: unpack(rows, 'TOTAL_INCOME'),
    text: unpack(rows, 'TOTAL_INCOME'),
    colorscale: [
      [1, 'rgb(241,248,233)'],
      [0.9, 'rgb(220,237,200)'],
      [0.8, 'rgb(197,225,165)'],
      [0.7, 'rgb(174,213,129)'],
      [0.6, 'rgb(156,204,101)'],
      [0.5, 'rgb(139,195,74)'],
      [0.4, 'rgb(124,179,66)'],
      [0.3, 'rgb(104,159,56)'],
      [0.2, 'rgb(85,139,47)'],
      [0.1, 'rgb(51,105,30)'],
      [0, 'rgb(27,94,32)']
    ],
    autocolorscale: false,
    reversescale: true,
    marker:{
      line:{
        color: 'rgb(100,100,100)',
        width: 0.5
      }
    },
    tick0: 0,
    zmin: 0,
    dtick: 1000,
    colorbar: {
      title: 'Income Scale',
      tickprefix: '$'
    }
  }];

  var layout = {
    title: 'US Income by zip codes',
    geo:{
      scope: 'usa',
      countrycolor: 'rgb(255,255,255)',
      showland: true,
      landcolor: 'rgb(217,217,217)',
      showlakes: true,
      lakecolor: 'rgb(255,255,255)',
      subunitcolor: 'rgb(255, 255, 255)',
      lonaxis: {},
      lataxis: {}
    }
  }

  Plotly.plot(choropleth, data, layout, {
      showLink: false
  });
});
