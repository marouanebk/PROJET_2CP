"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from rdv.views import (
    rdv
    ) 

from account.views import (
    home,
    # settings,
    ProfileUpdateView,
    prof,
    registration_view,
    account_view,
    logout_view,
    login_view,
    must_authenticate_view,
    registerlogin_view,
    activate_user,
)


urlpatterns = [
    path('',home , name = "home"),
    # path('settings/', settings, name="settings"),
    path('account/', account_view, name="account"),
    path('admin/', admin.site.urls),
    path('authen', registerlogin_view, name="registerlogin_view"),
    path('profile-update/<int:med_id>', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/<int:med_id>', prof, name='profile'),

    path('logout/' , logout_view, name="logout"),
    
    path('must_authenticate/', must_authenticate_view, name="must_authenticate"),
    path('register/', registration_view, name="register"),
    path('activate-user/<uidb64>/<token>',activate_user, name='activate'),


    path('rdv/', rdv, name="rdv"),

    path('admin/', admin.site.urls),
    path('', include('cal.urls')),
    path('', include('medecin.urls')),
    path('',include('historique.urls')),
    path('',include('staff.urls')),
    path('',include('annonce.urls')),


    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_form_password.html'), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset_form.html'), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
     name='password_reset_complete'),
    ]

from django.conf import settings 
from django.conf.urls.static import static    

urlpatterns +=  static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)
