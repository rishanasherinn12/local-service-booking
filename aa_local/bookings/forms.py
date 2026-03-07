from django import forms
from .models import Booking
from services.models import Worker
from datetime import datetime, timedelta
from bookings.models import Booking

class BookingAssignForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['worker']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # booking = kwargs.get('instance') #get current booking
        booking = self.instance
        #-------------------------
        if booking and booking.service:
            start = datetime.combine(
                booking.booking_date,
                booking.booking_time
            )

            duration = booking.service.duration_minutes
            end = start + timedelta(minutes=duration)

            # workers already booked in overlapping time
            busy_workers = Booking.objects.filter(booking_date=booking.booking_date,booking_status__in=["ASSIGNED","CONFIRMED","IN_PROGRESS"]
                                                  ).filter(
                                                    booking_time__lt=end.time(),
                                                    end_time__gt=booking.booking_time
                                                  ).values_list("worker",flat=True)
            # available workers
            available_workers = Worker.objects.filter(
                services=booking.service,
                is_active=True
            ).exclude(id__in=busy_workers)

            self.fields['worker'].queryset = available_workers
        #----------------------------------

        # if booking and booking.service:
        #     self.fields['worker'].queryset = Worker.objects.filter(
        #         services = booking.service, # Only workers who can do this service
        #         is_active = True
        #     )

         # Add styling cleanly
        self.fields['worker'].empty_label = "Select a worker"
        self.fields['worker'].widget.attrs.update({
            'class': 'form-control'
        }),
        

        if not self.fields['worker'].queryset.exists():
            self.fields['worker'].help_text = "No workers available for this service."
    
    def save(self, commit=True):
        booking = super().save(commit=False)
        
        if commit:
            booking.save()
        
        return booking