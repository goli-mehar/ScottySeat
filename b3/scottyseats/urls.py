from django.urls import path
from scottyseats import views

urlpatterns = [
    path('', views.mainmap, name='mainmap'),
    path('showmap', views.show_map, name='showmap'),
    path('inform', views.inform, name='inform'),
]

