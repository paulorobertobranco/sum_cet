from django.shortcuts import render
from app_load.src.app_load.load import list_input_files


def report_home(request):

    loaded_input_files, not_loaded_input_files = list_input_files()

    data = {
        'active_link': 'report',
        'loaded_input_files': loaded_input_files,
    }
    return render(request, 'app_report/select_database.html', data)


def show_report(request, database):
    data = {
        'selected_database': database.split('.')[0]
    }
    return render(request, 'app_report/report.html', data)
