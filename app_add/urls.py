from django.urls import path
from .views import select_database, show_database, add


urlpatterns = [
    path('', select_database, name='add_select'),
    path('<str:database>', show_database, name='show_database'),
    path('add/', add, name='add_failure'),
]
