from django.urls import path
from .views import predict_home


urlpatterns = [
    path('', predict_home, name='predict_select'),
]
