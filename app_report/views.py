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
    date_from, date_until, failures, month_range = get_features(database)

    data = {
        'active_link': 'report',
        'selected_database': database.split('.')[0],
        'failures': failures,
        'month_range': list(range(len(month_range))),
    }
    return render(request, 'app_report/report.html', data)
