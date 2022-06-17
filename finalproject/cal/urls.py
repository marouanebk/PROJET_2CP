from django.urls import include, re_path,path
from . import views

app_name = 'cal'
urlpatterns = [
    re_path(r'^index/$', views.index, name='index'),
    re_path(r'^calendar/$', views.CalendarViewNew.as_view(), name='calendar'),
    path("calenders/", views.CalendarView.as_view(), name="calendars"),

    path('event/new/<int:event_id>', views.event, name='event_new'),
	re_path(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    re_path(r'^all-event-list/$', views.AllEventsListView, name="all_events"),
    # path("all_event_list/", views.AllEventsListView.as_view, name="all_events"),
    # re_path(r'^event/approve/$', views.event_approve, name='event_approve'),


]
