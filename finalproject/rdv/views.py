from django.shortcuts import render, redirect
# from rdv.forms import RendezVousForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from cal.forms import RDVForm
from cal.models import RDV



def rdv(request, event_id=None):
    instance = RDV()
    if event_id:
        instance = get_object_or_404(RDV, pk=event_id)
    else:
        instance = RDV()

    form = RDVForm(request.POST or None, instance=instance ,initial={'Sender':request.user,'Phone_number':request.user.phone_number,'full_name':request.user.last_name+" "+request.user.first_name})

    if request.POST and form.is_valid():
        form.save()
        return HttpResponse('Request submitted')
    return render(request, 'rdv/cal.html', {'form': form})




