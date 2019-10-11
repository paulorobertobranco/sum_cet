from django.shortcuts import render, redirect
from .src.app_add.add import get_database_features, add_failure_to_database
from app_load.src.app_load.load import list_input_files


def select_database(request):
    loaded_input_files, not_loaded_input_files = list_input_files()
    data = {
        'active_link': 'add',
        'input_files': loaded_input_files + not_loaded_input_files,

    }

    return render(request, 'app_add/select_database.html', data)


def show_database(request, database):
    substations, failure_causes, tf_size, database_size, start_year, end_year, month_range = get_database_features(database)

    data = {
        'active_link': 'add',
        'selected_file': database,
        'last_year': end_year,
        'last_month': month_range[-1],
        'failure_causes': failure_causes,
        'substations': substations,
    }
    return render(request, 'app_add/show_database.html', data)


def add(request):
    loaded_input_files, not_loaded_input_files = list_input_files()
    loaded_input_files += not_loaded_input_files

    add_failure_to_database(request.POST)

    return redirect('add_select')
