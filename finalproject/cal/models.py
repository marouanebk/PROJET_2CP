from django.db import models
from django.urls import reverse
from account.models import Account
from datetime import datetime

class RDVManager(models.Manager):
    """ Event manager """

    def get_all_events(self, user):
        events = RDV.objects.filter(Receiver=user)
        return events

class RDV(models.Model):
    Sender                  = models.ForeignKey(Account, on_delete=models.CASCADE,related_name='Sender')
    Receiver                = models.ForeignKey(Account, on_delete=models.CASCADE,related_name='Receiver',limit_choices_to={'is_doctor': True},
)
    description = models.CharField(max_length=400)
    start_time = models.DateTimeField(null=True,blank=True)
    is_approved = models.BooleanField(default = False)
    objects = RDVManager()

    def __str__(self):
        return self.Sender.email

    def get_absolute_url(self):
        return reverse("calendarapp:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.start_time} </a>'

    @property
    def get_receiver(self):
        return self.Receiver
