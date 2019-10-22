var trace1 = {
  x: month_range,
  y: failures,
  mode: 'lines+markers',
  marker: {
    color: '#ff892e',
    size: 10
  }
};

var data = [trace1];

var layout = {
    xaxis: {
        title: 'FIC'
    },
    yaxis: {
        title: 'Mês'
    }
};

Plotly.newPlot('failure_plot', data, layout);
