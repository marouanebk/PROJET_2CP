from django.apps import AppConfig
from .models import Notification
from cal.models import RDV
from datetime import datetime, timedelta, date
from django.db.models import Q

def update():
    listt = RDV.objects.filter(Q(is_approved=True))
    for event in listt:
            if datetime.now().strftime("%Y-%m-%dT%H:%M:%S").split('T')[0] == event.start_time.strftime("%Y-%m-%dT%H:%M:%S").split('T')[0]:
                print(event.start_time.strftime("%Y-%m-%dT%H:%M:%S").split('T')[0],' ',datetime.now().strftime("%Y-%m-%dT%H:%M:%S").split('T')[0])
                noti = Notification.objects.create(to_user=event.Sender,from_user=event.Receiver,reminder=True)
                noti.save()