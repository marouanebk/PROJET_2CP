from django.shortcuts import render
from email import message
import imp
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q 
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from account.models import Account


def cal(request, pk ):
    med=Account.objects.all()
    print(med)
    context={'med':med}
    return render(request, 'calendrier/calendar.html' , context)

def home_page(request):
    #p = Pump()
    #p.getPumps()
    #pk = self.kwargs.get('pk')
    med= Account.objects.filter(is_doctor=True)
    context={'med': med}
    return render(request,"medecin/listmed.html",context)
    
def list_page(request):
    search_med = request.GET.get('search')
    page = request.GET.get('page')
    if search_med:
        listt = User.objects.filter(Q(username__icontains=search_med)|Q(first_name__icontains=search_med) & Q(is_doc=True))
    else:
        listt = User.objects.filter(Q(is_doc=True))
    p = Paginator(listt,1)
    try:
        listtt = p.get_page(page)
    except PageNotAnInteger:
        listtt = p.get_page(page)
    except EmptyPage:
        listtt = p.page(p.num_pages)
   
    return render(request,'medecin/listmed.html',{'listt' : listt,'listtt':listtt}) 
# Create your views here.
