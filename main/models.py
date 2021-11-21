from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank=True)
    location = models.CharField(max_length=100, blank=True)
    date = models.DateField()
    time = models.TimeField()
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


class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    # reputation
    def __str__(self):
        return self.username
