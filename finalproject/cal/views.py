from datetime import datetime, timedelta, date
from email.utils import parsedate
import json
from re import S
from sqlite3 import paramstyle
from stat import S_ENFMT
from time import time
from django.dispatch import receiver
from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from notifications.models import Notification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
import threading
from account.models import Account


import calendar

from .models import *
from .utils import Calendar
from .forms import RDVForm



class CalendarView(LoginRequiredMixin, generic.ListView):
    model = RDV
    template_name = "calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, event_id=None):
    sender = request.user
    receiver = get_object_or_404(Account,pk=event_id)
    if request.POST:
        print(receiver)
        desc = request.POST.get("description")
        date = request.POST.get("date")
        time = request.POST.get("time")
        print(desc)
        print(date)
        print(time)
        print(type(date))
        print(type(time))
        if desc and date and time:
            #s_time = parsedate(date+''+time+':00.000000')
            s_time = datetime.strptime(date+' '+time+':00.00000', '%Y-%m-%d %H:%M:%S.%f')
            print(s_time)
            print(type(s_time))
            rdv = RDV.objects.create(Sender=sender,Receiver=receiver,start_time=s_time,description=desc,is_approved=False)
            rdv.save()
            return render(request, 'cal/event.html', {'sender': sender,'receiver':receiver,'desc':desc})
    return render(request, 'cal/event.html',{'sender': sender,'receiver':receiver})  

def all_events(request):                                                                                                 
    all_events = RDV.objects.all()                                                                                    
    out = []                                                                                                             
    for event in all_events:  
        if event.is_approved==True:                                                                                           
            out.append(event)                                                                                                              
                                                                                                                     
    return JsonResponse(out, safe=False)  
class CalendarViewNew(generic.View):
    template_name = "calendarapp/calendar.html"
    form_class = RDVForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        events = RDV.objects.get_all_events(user=request.user)
        event_list = []
        # start: '2020-09-16T16:00:00'

        for event in events:
            if event.is_approved==True:
                event_list.append(
                    {
                        "title":event.Sender.first_name +" Num : "+str(event.Sender.phone_number),
                        "start":event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "url":reverse('cal:event_edit', args=(event.id,))                        
                    }
                )
        context = {"form": forms, "events": event_list}
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("cal:calendar")
        context = {"form": forms}
        return render(request, self.template_name, context)


def AllEventsListView(request):
    template_name = "calendarapp/events_list.html"
    if request.POST:
        print(request.POST.get("approve"))
        event = get_object_or_404(RDV , pk=request.POST.get("approve"))
        print(event.id)
        print(event.is_approved)
        print(event.is_approved)
        if not event.is_approved:
            event = get_object_or_404(RDV , pk=request.POST.get("approve"))
            event.is_approved = True
            event.save()
            noti = Notification.objects.create(to_user=event.Sender,from_user=request.user)
            noti.save()
            user = event.Sender 
            receiver = event.Receiver
            date = event.start_time
            send_email(user, request, receiver , date)
        events = RDV.objects.filter(Q(Receiver = request.user)& Q(is_approved= False))
        return render (request,template_name, {'events': events})
    else :
        events = RDV.objects.filter(Q(Receiver = request.user)& Q(is_approved= False))
    return render (request,template_name, {'events': events})

def index(request):
    return HttpResponse('hello')

def Calender(request):
    return render(request,"calendar.html")


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_email(user, request , receiver , date):
    current_site = get_current_site(request)
    email_subject = 'Approval'
    email_body = render_to_string('calendarapp/email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'receiver': receiver,
        'date':date,
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )

    # if not settings.TESTING:
    EmailThread(email).start()

