
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [ 
    path('cal/',views.cal , name= 'cal'),
    # path('medecin/home/',views.home_page,name= 'homepage'),
    path('listpage/', views.home_page, name='listpage'),
]