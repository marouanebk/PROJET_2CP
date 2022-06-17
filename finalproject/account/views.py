from calendar import c
from cmath import log
from pickle import GET
import re
from webbrowser import get
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.utils.functional import lazy
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from cal.models import RDV
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading
from .models import Account
from django.urls import reverse
from .forms import UserForm, ProfileForm
from django.views.generic import TemplateView, CreateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin



class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('account/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )

    # if not settings.TESTING:
    EmailThread(email).start()


def home (request):
	return render(request , "account/index.html",)
def registerlogin_view(request):
	context = {}
	user = request.user
	if user.is_authenticated:
		return redirect("home")
	if request.POST:
		register_form = RegistrationForm(request.POST)
		login_form = AccountAuthenticationForm(request.POST)
		if register_form.is_valid():
			register_form.is_active=True
			register_form.save()



			email = register_form.cleaned_data.get('email')
			raw_password = register_form.cleaned_data.get('password1')
			# account = authenticate(email=email, password = raw_password)
			user = Account.objects.get(email=email)
			send_activation_email(user, request)

			return redirect('home')
			# login(request, account)
			# return redirect('home')
		elif login_form.is_valid(): 
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)
		# elif not login_form.is_valid():
		# 	print(login_form.errors.as_data) 
			messages.success(request,'red')
			if user is not None:
				login(request, user)
				return redirect("home")	
		elif not login_form.is_valid():
			context['registration_form'] = register_form
			messages.success(request,'veuillez verifier les informations entreés')	
		elif not register_form.is_valid():
			print('kys')
			messages.success(request,'blue')	
			return render(request, 'account/newlogin.html', context)
	else:
		register_form = RegistrationForm()
		context['registration_form'] = register_form
		login_form = AccountAuthenticationForm()

	context['login_form'] = login_form
	return render(request, 'account/newlogin.html', context)


def registration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('home')
		else:
			context['registration_form'] = form


	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)

def login_view(request):
	context = {}
	user = request.user
	if user.is_authenticated: 
		return redirect("home")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			print("fform is valid ")

			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("home")
		else:
			print("")
	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	# print(form)
	return render(request, "account/login.html", context)

def logout_view(request):
	logout(request)
	return redirect('/')

def account_view(request):

	if not request.user.is_authenticated:
			return redirect("login")

	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			print('form is valid')
			form.initial = {
					"email": request.POST['email'],
					"first_name": request.POST['first_name'],
					"last_name": request.POST['last_name'],
					"phone_number": request.POST['phone_number'],
					"place_of_birth": request.POST['place_of_birth'],
					"profile_picture":request.POST['profile_picture'],

			}
			form.save()
			context['success_message'] = "Updated"
	else:
		form = AccountUpdateForm(

			initial={
					"email": request.user.email, 
					"first_name":request.user.first_name,
					"last_name":request.user.last_name,
					"phone_number":request.user.phone_number,
					"profile_picture":request.user.profile_picture,
					# "place_of_birth":request.user.

				}
			)

	context['account_form'] = form

	# blog_posts = BlogPost.objects.filter(author=request.user)
	# context['blog_posts'] = blog_posts

	return render(request, "account/account.html", context)


def must_authenticate_view(request):
	return render(request, 'account/must_authenticate.html', {})

def activate_user(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print("iud")

        print("after uid")

        user = Account.objects.get(pk=uid)

        print(user)
    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.is_active = True
        user.save()
        messages.add_message(request, messages.SUCCESS,'Email verified, you can now login')
        return redirect(reverse('registerlogin_view'))

    # return render(request, 'account/activate-failed.html', {"user": user})
    return redirect (reverse('registerlogin_view'))

def prof (request,med_id):
	med = get_object_or_404(Account,pk=med_id)
	return render(request , "account/profile.html",{"med":med})


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'account/edit.html'

    def post(self, request,med_id):

        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return HttpResponseRedirect(reverse('profile', args=[1]))

        context = self.get_context_data(
                                        user_form=user_form,
                                        profile_form=profile_form
                                    )

        return self.render_to_response(context)     

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)



