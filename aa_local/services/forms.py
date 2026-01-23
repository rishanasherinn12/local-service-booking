from django import forms
from .models import Worker

class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['full_name','role','phone','photo','is_active']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone)<10:
            raise forms.ValidationError("Phone no must contain only digits")
        
        return phone