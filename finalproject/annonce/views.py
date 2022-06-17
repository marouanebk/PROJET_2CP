from .models import forum
from .forms import Annonce
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404




# Create your views here.
def GeneralInfo(request):
	annonces = forum.objects.all()
	context = {'posts' : annonces}
	return render(request, "forum/forum.html" , context)

def Subjects(request):
	return render(request, "forum/post.html")

def Posts(request , subject_name):
	context ={}
	all_posts = forum.objects.filter(status=subject_name)
	context = {'posts':all_posts}
	return render(request, "forum/detail.html" , context)

def post_detail(request, post_id):
    instance = forum()
    if post_id:
        instance = get_object_or_404(forum, pk=post_id)
    else:
        instance = Account()

    return render(request, 'forum/detail1.html', {'post': instance})


def new(request):
	form = Annonce(request.POST or None,initial={'Author':request.user})

	if request.POST and form.is_valid():
		form.save()
		return HttpResponseRedirect(reverse('home'))

	context = {'form': Annonce}
	return render (request, "forum/new.html" , context)


