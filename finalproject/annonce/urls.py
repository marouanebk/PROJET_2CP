from django.urls import include, re_path,path
from . import views

app_name = 'annonce'
urlpatterns = [
    path('general_info/', views.GeneralInfo , name="general_info"),
    path('subjects/' ,views.Subjects , name="subjects"),
    # path('subjects/posts' , views.Posts , name="posts"),
    re_path(r'^subjects/(?P<subject_name>\d+)/$', views.Posts, name='posts'),
    path('subjects/new' , views.new , name="new"),
    re_path(r'^post/detail/(?P<post_id>\d+)/$', views.post_detail, name='post_detail'),


]
