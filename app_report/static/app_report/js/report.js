var trace1 = {
  x: month_range,
  y: failures_by_month,
  mode: 'lines+markers',
  marker: {
    color: '#ff892e',
    size: 8
  }
};

var data = [trace1];

var layout = {
    xaxis: {
        title: 'Mẽs'
    },
    yaxis: {
        title: 'FIC'
    }
};

Plotly.newPlot('failure_by_month_plot', data, layout);

var trace1 = {
  x: causes,
  y: failures_by_causes,
  type: 'bar',
   marker: {
    color: '#ff892e'
  }
};

var data = [trace1];

var layout = {
    xaxis: {
        title: 'Causa de Falha',
        showticklabels: false
    },
    yaxis: {
        title: 'FIC'
    }
};

Plotly.newPlot('failure_by_cause_plot', data, layout);
