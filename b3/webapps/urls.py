from scottyseats import views
from django.urls import path, include

urlpatterns = [
    path('', views.mainmap),
    path('scottyseats/', include('scottyseats.urls')),
]