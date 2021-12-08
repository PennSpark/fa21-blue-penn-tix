
from django.contrib.auth.models import User

from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank=True)
    location = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField()
    num_tickets = models.IntegerField(default=0)
    # TODO: add num_tickets

    def __str__(self):
        return self.name

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField(default=1)
    # TODO: add optional description/other notes
    sold = models.BooleanField(default=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.event.name



