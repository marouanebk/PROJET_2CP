from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from account.views import home
from .models import request_doc
from django.db.models import Q
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
import threading
from account.models import Account


from .forms import request_docForm

from account.models import Account
# Create your views here.
from account.views import *

from account.forms import admin_editForm

def admin_view(request):
    # if request.user.is_admin==False:
    #   return redirect(request , "home" )
    user = request.user
    if user.is_staff == False:
        return HttpResponseRedirect(reverse('home'))
    users = Account.objects.filter(is_doctor=False, is_assistant=False , is_admin=False , is_staff=False)
    context = {"users":users}
    return render(request, "admin/admin.html" , context)

def doctors_view(request):
    users = Account.objects.filter(is_doctor=True)
    context = {"users":users}
    return render(request, "admin/doctors.html" , context)

def assistante_view(request):
    users = Account.objects.filter(is_assistant=True)
    context = {"users":users}
    return render(request, "admin/assistante.html" , context)


def submit_request(request, event_id=None):
    # if request.user.request_doc.exist:
    #     return HttpResponseRedirect(reverse('home'))
    owner = request.user
    if request.POST:

        # print("method = post")
        Speciality = request.GET.get("specialty")
        # print(Speciality)

        Location = request.GET.get("location")
        Description = request.GET.get("description")
        # # if Description:
        #     request_d = request_doc.objects.create(owner=Owner) 
        #     request_d.save()
        # else:
        #     print("error")
        request_d = request_doc.objects.create(owner=owner) 
        request_d.description = request.POST.get("description")
        request_d.speciality = request.POST.get("speciality")
        request_d.location = request.POST.get("location")
        request_d.exist=True
        request_d.save()
        return HttpResponseRedirect(reverse('home'))
    else :
        print("method not post")
    return render(request, 'admin/log.html', {'form': owner})


def user_ed(request,user_id=None):
    instance = Account()
    if user_id:
        instance = get_object_or_404(Account, pk=user_id)
    else:
        instance = Account()

    form = admin_editForm(request.POST or None, instance=instance)

    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('staff:admin_view'))
    return render(request, 'admin/edit.html', {'form': form})

def visualise_requests(request):
    user = request.user

    if user.is_staff == False:
        return HttpResponseRedirect(reverse('home'))
    # users = Account.objects.filter(is_patient=True)
    users = request_doc.objects.filter(exist=True)
    # events = RDV.objects.filter(Q(Receiver = request.user)& Q(is_approved= False))

    context = {"users":users}
    return render(request, "admin/requests.html" , context)


def user_approve(request,user_id=None):
    instance = Account()
    if user_id:
        instance = get_object_or_404(Account, pk=user_id)
    else:
        instance = Account()

    form = admin_editForm(request.POST or None, instance=instance)

    if request.POST and form.is_valid():
        form.save()
        instance = get_object_or_404(Account, pk=user_id)

        if instance.is_doctor:
            print("instance is doctor ")
            email = instance.email
            user = Account.objects.get(email=email) 
            send_email(user, request)
            print("Here u send ur email ")
        return HttpResponseRedirect(reverse('staff:admin_view'))
    return render(request, 'admin/approve.html', {'form': form})


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_email(user, request , receiver , date ):
    current_site = get_current_site(request)
    email_subject = 'Promotion'
    email_body = render_to_string('admin/new_doc.html', {
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
