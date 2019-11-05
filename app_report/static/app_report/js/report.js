var cl1 = {
    x: cl1_plot_x,
    y: cl1_plot_y,
    mode: 'markers',
    type: 'scatter',
    name: 'cluster 1',
    marker: {
        size: 10,
        color: 'hex(4c1130ff)',
    }
};

var cl2 = {
    x: cl2_plot_x,
    y: cl2_plot_y,
    mode: 'markers',
    type: 'scatter',
    name: 'cluster 2',
    marker: {
    size: 10,
    color: 'hex(ff892e)',
    }
};

var cl3 = {
    x: cl3_plot_x,
    y: cl3_plot_y,
    mode: 'markers',
    type: 'scatter',
    name: 'cluster 3',
    marker: { size: 10 }
};

var data = [ cl1, cl2, cl3 ];

var layout = {

};

Plotly.newPlot('cluster_plot', data, layout);

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
    visible: true,
    type: 'bar',
    marker: {
        color: '#ff892e'
    }
};

var month_data = {
    x: failures_plot['months']['x'],
    y: failures_plot['months']['y'],
    type: 'bar',
    visible: false,
    marker: {
        color: '#ff892e'
    }
};

var substation_data = {
    x: failures_plot['substations']['x'],
    y: failures_plot['substations']['y'],
    type: 'bar',
    visible: false,
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
    xaxis: {
        title: 'Falha',
        showticklabels: false
    },
    updatemenus: [{
        x:1,
        y: 1.3,
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

Plotly.newPlot('failure_by_cause_plot', data, layout);


