from django import forms


class NewTicketForm(forms.Form):
    event_name = forms.CharField(label="Event Name", max_length=100)
    event_date = forms.DateField(label="Event Date")
    event_time = forms.TimeField(label="Event Time")
    quantity = forms.IntegerField(label="Quantity")
    price = forms.DecimalField(label="Price", max_digits=6, decimal_places=2)
