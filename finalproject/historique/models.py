from datetime import datetime
from django.utils import timezone
from operator import mod
from django.db import models
from cal.models import RDV
from annoying.fields import AutoOneToOneField
class history(models.Model):
    rendez_vous = AutoOneToOneField(RDV,on_delete=models.CASCADE,related_name='rendez_vous')
    observation = models.TextField(null=True)
    diagnostique = models.TextField(null=True)
    lettre = models.TextField(null=True)
