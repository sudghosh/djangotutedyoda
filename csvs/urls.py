from django.urls import path
from .views import data_upload_view

app_name = 'csvs'

urlpatterns = [
    path('',data_upload_view,name='data_upload_view'),
]