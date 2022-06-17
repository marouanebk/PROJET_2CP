from django.urls import include, re_path,path
from . import views

app_name = 'staff'
urlpatterns = [
    path('staff/', views.admin_view , name="admin_view"),
    path('staff/doctors/' ,views.doctors_view, name="doctors_view"),
    path('staff/assistante/' , views.assistante_view , name="assistante_view"),
    re_path(r'^staff/edit/(?P<user_id>\d+)/$', views.user_ed, name='user_edit'),
    path('request/' ,views.submit_request, name='submit_request'),
    path('staff/requests/' , views.visualise_requests, name='visualise_requests'),
    re_path(r'^staff/approve/(?P<user_id>\d+)/$', views.user_approve, name='user_approve'),


    

]
