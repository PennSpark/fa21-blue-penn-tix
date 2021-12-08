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

            event.num_tickets += form.cleaned_data["quantity"]
            if form.cleaned_data["price"] < event.lowest_ticket_price or event.lowest_ticket_price < 0:
                event.lowest_ticket_price = form.cleaned_data["price"]
            event.save()

            new_ticket = Ticket(seller=request.user)
            new_ticket.event = event
            new_ticket.price = form.cleaned_data["price"]
            
            new_ticket.quantity = form.cleaned_data["quantity"]
            new_ticket.event = event
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
    tickets = Ticket.objects.all().order_by("price").filter(seller=user)
    return render(request, "profile.html", {"user": user, "tickets": tickets})


def sell_ticket_from_event_view(request):
    sell_ticket(request.GET['id'])
    event_id = request.GET['event_id']
    return redirect("/event?id=" + event_id)

def sell_ticket_from_profile_view(request):
    sell_ticket(request.GET['id'])
    return redirect("/profile")

def sell_ticket(id):
    ticket = Ticket.objects.get(id=id)
    event = ticket.event
    ticket.quantity -= 1
    ticket.save()
    ticket.event.num_tickets -= 1
    ticket.event.save()
    print(ticket.quantity)
    if ticket.quantity <= 0:
        ticket.delete()
        tickets = Ticket.objects.all().order_by("price").filter(event=event)
        print("got here:")
        print(tickets)
        if len(tickets) > 0:
            ticket.event.lowest_ticket_price = tickets[0].price
            ticket.event.save()

def add_ticket_view(request):
    if request.method == "POST":
        event = Event.objects.get(id=request.POST["event"])
        ticket = Ticket.objects.create(
            event=event, seller=request.user, price=request.POST["price"], sold=0
        )
        ticket.save()

    return redirect("/")  # change this redirect

def event_view(request):
    event = Event.objects.get(id=request.GET["id"])
    tickets = Ticket.objects.all().order_by("price").filter(event=event)
    return render(request, "event.html", {"event": event, "tickets": tickets})

def tickets_view(request):
    tickets = Ticket.objects.all().order_by("price")
    return render(request, "tickets.html", {"tickets": tickets})


def main_view(request):
    if not request.user.is_authenticated:
        return render(request, "splash.html")

    events = Event.objects.all().order_by("date")
    for event in events:
        if event.num_tickets <= 0:
            event.delete()
    events = Event.objects.all().order_by("date")

    return render(request, "main.html", {"events": events})


def user_profile_view(request):
    user = User.objects.get(username=request.GET["username"])
    tickets = Ticket.objects.all().order_by("event").filter(seller=user)
    return render(request, "user.html", {"user": user, "tickets": tickets})


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
    username = request.POST["username"]
    password=request.POST["password"]
    email=request.POST["email"]
    first_name=request.POST["first name"]
    last_name=request.POST["last name"]

    if len(username) > 0 and len(password) > 0 and len(email) > 0 and len(first_name) > 0 and len(last_name) > 0:
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        login(request, user)
        return redirect("/")
    else:
        return redirect("/splash?error=SignupError")


def logout_view(request):
    logout(request)
    return redirect("/splash")
