from django.db import models
from account.models import Account

SPECIALITY = ((0, "blank"), (1, "speciality1") , (2, "speciality2") , (3, "speciality3") )


class request_doc(models.Model):
	owner    = models.OneToOneField(Account, on_delete=models.CASCADE,related_name='owner')
	description = models.CharField(max_length=500,blank=True,null=True)
	speciality = models.CharField(max_length=400,blank=True,null=True)
	location = models.CharField(max_length=400,blank=True,null=True)
	# is_approved = models.BooleanField(default=False)
	exist 	= models.BooleanField(default=False)




	def __str__(self):
		return self.owner.first_name
