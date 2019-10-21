from django.shortcuts import render
from django.http import JsonResponse
from .src.app_load.load import list_input_files, get_dataset_features, run


def select_database(request):
    loaded_input_files, not_loaded_input_files = list_input_files()
    data = {
        'active_link': 'load',
        'loaded_input_files': loaded_input_files,
        'not_loaded_input_files': not_loaded_input_files
    }
    return render(request, 'app_load/select_database.html', data)


def load_features(request, database):
    _, failure_causes, tf_size, database_size, start_year, end_year, month_range = get_dataset_features(database)
    data = {
        'active_link': 'load',
        'tf_size': tf_size,
        'database_size': database_size,
        'range_clusters': range(1, 5),
        'selected_database': database,
        'failure_causes': enumerate(failure_causes),
        'month_range': month_range,
        'start_year': start_year,
    }
    return render(request, 'app_load/load.html', data)


def load(request):

    auto_cluster = request.POST['auto_cluster'] in 'true'
    database = request.POST['database_name']
    train_size = int(request.POST['train_size'])
    clusters = request.POST['clusters']

    if auto_cluster:
        run(database, train_size)
    else:
        print(auto_cluster)
        run(database, train_size, clusters=clusters)

    return JsonResponse({'status': True})

