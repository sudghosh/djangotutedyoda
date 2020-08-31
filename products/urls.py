from django.urls import path
from .views import chart_select_view, add_purchase_view, sales_dist_view

app_name = 'products'

urlpatterns = [
    path('',chart_select_view,name='chart_select_view'),
    path('add/',add_purchase_view,name='add_purchase_data'),
    path('sales/',sales_dist_view,name='sales_view'),
]