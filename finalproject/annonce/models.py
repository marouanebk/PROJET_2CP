from django.db import models
from account.models import Account
# from .models import Commentaire

# Create your models here.

STATUS = ((0, "blank"), (1, "medcin") , (2, "malady") , (3, "Medicament") , (4, "site") )


class forum(models.Model):
	Author 	= models.ForeignKey(Account ,on_delete=models.CASCADE,related_name='Author')
	date  	= models.DateTimeField(auto_now_add=True)
	title 	= models.CharField(max_length=200)
	f_description = models.TextField()
	is_general_info = models.BooleanField(blank=True,null=True, default=False)
	status = models.IntegerField(choices=STATUS, default=0)



	def __str__(self):
		return self.title

class Commentaire(models.Model):
	post 			= models.ForeignKey(forum, on_delete=models.CASCADE , related_name="post")
	author_c		= models.ForeignKey(Account, on_delete=models.CASCADE, related_name="author_c")
	c_description 	= models.TextField()
	date  			= models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.c_description






