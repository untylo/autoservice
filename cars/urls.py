from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name='home'),
    path('brands/', brand_list, name='brand_list'),
    path('brands/add/', brand_add, name='brand_add'),
    path('brands/<int:brand_id>/add-model/', model_add, name='model_add'),
    path('clients/', client_list, name='client_list'),
    path('clients/add/', client_add, name='client_add'),
    path('clients/<int:client_id>/add-car/', car_add, name='car_add'),
    path('ajax/load-models/', load_models, name='ajax_load_models'),
    path("cars/", car_list, name="car_list"),
    path("cars/ajax/", car_list, name="car_list_ajax"),  # AJAX filtering
    ]
