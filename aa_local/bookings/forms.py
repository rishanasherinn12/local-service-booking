from django import forms
from .models import Booking
from services.models import Worker

class BookingAssignForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['worker']

    def __init__(self, *args, **kwargs):
        booking = kwargs.get('instance') #get current booking
        super().__init__(*args, **kwargs)
        

        if booking:
            self.fields['worker'].queryset = Worker.objects.filter(
                services = booking.service, # Only workers who can do this service
                is_active = True
            )

         # Add styling cleanly
        self.fields['worker'].widget.attrs.update({
            'class': 'form-control'
        }),
        self.fields['worker'].empty_label = "Select a worker"

        if not self.fields['worker'].queryset.exists():
            self.fields['worker'].help_text = "No workers available for this service."
    
    def save(self, commit=True):
        booking = super().save(commit=False)
        booking.booking_status = "ASSIGNED"

        if commit:
            booking.save()
        
        return booking