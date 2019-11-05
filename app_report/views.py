import json
from django.shortcuts import render
from app_load.src.app_load.load import list_input_files
from app_report.src.app_report.report import get_features


def report_home(request):

    loaded_input_files, not_loaded_input_files = list_input_files()

    data = {
        'active_link': 'report',
        'loaded_input_files': loaded_input_files,
    }
    return render(request, 'app_report/select_database.html', data)


def show_report(request, database):
    len_db, len_tfs, failures_by_month, failures_plot, month_range, clusters, cl_plot = get_features(database)
    data = {
        'active_link': 'report',
        'cl1_plot_x': json.dumps(list(cl_plot[cl_plot['cluster_id'] == 0][0])),
        'cl1_plot_y': json.dumps(list(cl_plot[cl_plot['cluster_id'] == 0][1])),
        'cl2_plot_x': json.dumps(list(cl_plot[cl_plot['cluster_id'] == 1][0])),
        'cl2_plot_y': json.dumps(list(cl_plot[cl_plot['cluster_id'] == 1][1])),
        'cl3_plot_x': json.dumps(list(cl_plot[cl_plot['cluster_id'] == 2][0])),
        'cl3_plot_y': json.dumps(list(cl_plot[cl_plot['cluster_id'] == 2][1])),
        'selected_database': database.split('.')[0],
        'failures_by_month': failures_by_month,
        'failures_plot': json.dumps(failures_plot),
        'clusters': enumerate(clusters),
        'month_range': list(range(len(month_range))),
        'database_size': len_db,
        'tf_size': len_tfs,
    }
    return render(request, 'app_report/report.html', data)
