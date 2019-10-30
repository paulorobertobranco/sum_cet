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
    len_db, len_tfs, failures_by_month, failures_plot, month_range, clusters = get_features(database)
    data = {
        'active_link': 'report',
        'selected_database': database.split('.')[0],
        'failures_by_month': failures_by_month,
        'failures_plot': json.dumps(failures_plot),
        'clusters': enumerate(clusters),
        'month_range': list(range(len(month_range))),
        'database_size': len_db,
        'tf_size': len_tfs,
    }
    return render(request, 'app_report/report.html', data)
