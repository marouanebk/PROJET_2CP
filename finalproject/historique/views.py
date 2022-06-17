from calendar import c
from ctypes import alignment
from datetime import datetime
from email.utils import parsedate
import imp
from itertools import starmap
from django.http import request,FileResponse
from django.shortcuts import render,get_object_or_404
from .models import history
from account.models import Account
from django.db.models import Q 
from .forms import ordoForm
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch,cm
from reportlab.lib.pagesizes import letter
from cal.models import RDV
from django.utils import timezone
def hist(request):
    search_name = request.GET.get('search_name')
    search_date = request.GET.get('search_date')
    search_hour = request.GET.get('search_hour')
    search_ville = request.GET.get('search_ville')
    page = request.GET.get('page')
    listt = RDV.objects.filter(Q(start_time__lte= datetime.now())).order_by('-start_time')
    for e in listt:
        print(e.rendez_vous)
    if search_name or search_ville:
        listt = listt.filter(Q(Sender__first_name__icontains=search_name) | Q(Sender__last_name__icontains=search_name))
    if search_date:
        search_date1 = datetime.strptime(search_date+' 00:00:00.00000', '%Y-%m-%d %H:%M:%S.%f')
        print(search_date1.day)
        listt = listt.filter(Q(start_time__year__icontains=search_date1.year)&Q(start_time__month__icontains=search_date1.month) & Q(start_time__day__icontains=search_date1.day))        
    return render(request,'history/historique.html',{'listt' : listt})
def hist_perso(request,id):
    if id:
        instance = get_object_or_404(Account, pk=id)
    historique_perso = RDV.objects.filter(Q(Receiver=request.user)&Q(Sender__id=id)).order_by('-start_time')
    return render(request,'history/hist_personel.html',{'hperso': historique_perso,'patient':instance})
def ordonance(request,history_id):
    his = get_object_or_404(history,pk=history_id)
    form = ordoForm(request.POST or None,instance=his)
    if form.is_valid():
        form.save()
    return render(request,'history/ordo.html',{'historique':his,'form':form})

def ordo_pdf(request,his_id):
    _W, _H = (21*cm, 29.7*cm)
    A6 = (_W*.5, _H*.5)
    buf = io.BytesIO()
    p = canvas.Canvas(buf,pagesize=A6,bottomup=0)
    textob = p.beginText()
    textob.setTextOrigin(cm,cm)
    textob.setFont("Helvetica",12)
    ins = get_object_or_404(history,pk=his_id)
    lines = [
            "                      ORDONNANCE",
            "",
            "De la part du Dr. ____________.",
            "Spécialité : _____________.",
            "Jour : " +ins.rendez_vous.start_time.strftime("%Y-%m-%d"),
            "",
            "",
           ins.observation
           
    ]
    for line in lines:
        textob.textLine(line)
    p.drawText(textob)
    p.showPage()
    p.save()
    buf.seek(0)
    return FileResponse(buf,as_attachment=True,filename="ordo.pdf")
# Create your views here.