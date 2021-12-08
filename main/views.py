from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from main.models import Event, Ticket
from django.http import HttpResponse
from .forms import NewTicketForm
from datetime import datetime
from django.utils.timezone import make_aware


def sell_view(request):
    if not request.user.is_authenticated:
        return render(request, "splash.html")
        
    if request.method == "POST":
        form = NewTicketForm(request.POST)
        if form.is_valid():
            try:
                event = Event.objects.get(
                    name=form.cleaned_data["event_name"],
                    date=make_aware(
                        datetime.combine(
                            form.cleaned_data["event_date"],
                            form.cleaned_data["event_time"],
                        )
                    ),
                )
            except Event.DoesNotExist:
                event = Event()
                event.name = form.cleaned_data["event_name"]
                event.date = make_aware(
                    datetime.combine(
                        form.cleaned_data["event_date"], form.cleaned_data["event_time"]
                    )
                )
                event.save()

            new_ticket = Ticket(seller=request.user)
            new_ticket.event = event
            new_ticket.price = form.cleaned_data["price"]
            new_ticket.quantity = form.cleaned_data["quantity"]
            new_ticket.save()
            ##TODO: add something here that gives confirmation your ticket has been posted
            return HttpResponseRedirect("/")
    else:
        form = NewTicketForm()

    return render(request, "sell.html", {"form": form})


def profile_view(request):
    if not request.user.is_authenticated:
        return render(request, "splash.html")

    user = request.user
    #tickets = Ticket.objects.all().order_by("price").filter(seller=user)
    #user.tickets = tickets

    return render(request, "profile.html", {"user": user})

def sell_ticket(request):
    ticket = Ticket.objects.get(id=request.GET['id'])
    ticket.quantity -= 1
    ticket.save()
    if ticket.quantity <= 0:
        ticket.delete()

    return redirect("/profile.html")

def add_ticket_view(request):
    if request.method == "POST":
        event = Event.objects.get(id=request.POST["event"])
        ticket = Ticket.objects.create(
            event=event, seller=request.user, price=request.POST["price"], sold=0
        )
        ticket.save()

    return redirect("/")  # change this redirect


def tickets_view(request):
    tickets = Ticket.objects.all().order_by("price")

    return render(request, "tickets.html", {"tickets": tickets})


def main_view(request):
    if not request.user.is_authenticated:
        return render(request, "splash.html")

    events = Event.objects.all().order_by("date")
    return render(request, "main.html", {"events": events})


def delete_view(request):
    ticket = Ticket.objects.get(id=request.GET["id"])
    if ticket.seller == request.user:
        ticket.delete()
    return redirect("/")  # change this redirect


def splash_view(request):
    return render(request, "splash.html")


def login_view(request):
    username, password = request.POST["username"], request.POST["password"]
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect("/")
    else:
        return redirect("/splash?error=LoginError")


def signup_view(request):
    user = User.objects.create_user(
        username=request.POST["username"],
        password=request.POST["password"],
        email=request.POST["email"],
        first_name=request.POST["first name"],
        last_name=request.POST["last name"],
    )
    login(request, user)
    return redirect("/")


def logout_view(request):
    logout(request)
    return redirect("/splash")
