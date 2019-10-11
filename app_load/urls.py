from django.urls import path
from .views import select_database, load_features, load


urlpatterns = [
    path('', select_database, name='load_select'),
    path('<str:database>', load_features, name='load_features'),
    path('run/', load, name='run_load'),
]
