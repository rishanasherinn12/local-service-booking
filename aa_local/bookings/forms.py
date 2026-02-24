from django import forms
from .models import Booking
from services.models import Worker

class BookingAssignForm(forms.ModelForm):
    worker = forms.ModelChoiceField(
        queryset=Worker.objects.filter(is_active = True),
        empty_label="Select a worker..",
        widget=forms.Select(attrs={'class':'form-control'}))
    
    class Meta:
        model = Booking
        fields = ['worker']
    
    def save(self, commit=True):
        booking = super().save(commit=False)
        booking.status = "CONFIRMED"

        if commit:
            booking.save()
        
        return booking