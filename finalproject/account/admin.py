from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account, Profile
from annonce.models import forum,Commentaire
from staff.models import request_doc


# class AccountAdmin(UserAdmin):
# 	list_display = ('email','phone_number','first_name','last_name','is_patient','is_doctor','is_admin','is_staff')
# 	search_fields = ('email', 'phone_number')
# 	readonly_fields=('date_joined', 'last_login')
# 	ordering = ('email',)

# 	filter_horizontal = ()
# 	list_filter = ()
	# # fieldsets = ()
# class RDVDisplay(UserAdmin):
# 	list_display = ('Sender', 'receiver', 'time')
# 	search_fields = ('Sender', 'receiver')

# 	filter_horizontal = ()
# 	list_filter = ()
# 	fieldsets = ()


admin.site.register(Account)
admin.site.register(forum)
admin.site.register(Commentaire)
admin.site.register(request_doc)
admin.site.register(Profile)



