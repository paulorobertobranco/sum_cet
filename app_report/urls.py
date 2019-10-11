from django.urls import path
from .views import report_home, show_report


urlpatterns = [
    path('', report_home, name='report_select'),
    path('<str:database>', show_report, name='show_report')
]
