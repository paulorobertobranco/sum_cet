from django.urls import path
from .views import predict_home, show_predict


urlpatterns = [
    path('', predict_home, name='predict_select'),
    path('<str:database>', show_predict, name='show_predict'),
]
