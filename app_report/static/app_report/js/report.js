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
    },
};

Plotly.newPlot('failure_by_month_plot', data, layout);

var cause_data = {
    x: failures_plot['causes']['x'],
    y: failures_plot['causes']['y'],
    type: 'bar',
    marker: {
        color: '#ff892e'
    }
};

var month_data = {
    x: failures_plot['months']['x'],
    y: failures_plot['months']['y'],
    type: 'bar',
    marker: {
        color: '#ff892e'
    }
};

var substation_data = {
    x: failures_plot['substations']['x'],
    y: failures_plot['substations']['y'],
    type: 'bar',
    marker: {
        color: '#ff892e'
    }
};

var data = [cause_data, month_data, substation_data];

var layout = {
    showlegend: false,
    yaxis: {
        title: 'FIC'
    },
    updatemenus: [{
        x:1,
        y: 1.5,
        yanchor: 'top',
        buttons: [{
            method: 'update',
            args: [
                {'visible': [true, false, false]},
                {'xaxis': {
                            'title': 'Falha',
                            'showticklabels': false
                          }
                }
            ],
            label: 'Causa de Falha'
        }, {
            method: 'update',
            args: [
                {'visible': [false, true, false]},
                {'xaxis': {
                            'title': 'Mês',
                            'showticklabels': false
                            }
                }
            ],
            label: ' Mês'
        },
        {
            method: 'update',
            args: [
                {'visible': [false, false, true]},
                {'xaxis': {
                            'title': 'Substação',
                            'showticklabels': false
                          }
                }
            ],
            label: ' Substação'
        }]
    }]
};

Plotly.plot('failure_by_cause_plot', data, layout);
