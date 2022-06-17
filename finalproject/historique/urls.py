from django.urls import include, re_path,path
from .views import hist,hist_perso, ordo_pdf,ordonance

app_name = 'historique'
urlpatterns = [

path('historique',hist,name='historique'),
path('hist_perso/<int:id>',hist_perso,name='historique personel'),
path('ordo/<int:history_id>',ordonance,name='ordonance'),
path('pdf_ordo/<int:his_id>',ordo_pdf,name='pdf ordo'),]