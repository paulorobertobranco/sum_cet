from django.shortcuts import render
from app_load.src.app_load.load import list_input_files


def predict_home(request):

    loaded_input_files, not_loaded_input_files = list_input_files()

    data = {
        'active_link': 'predict',
        'loaded_input_files': loaded_input_files,
    }
    return render(request, 'app_predict/select_database.html', data)


def show_predict(request, database):
    return render(request, 'app_predict/predict.html')
