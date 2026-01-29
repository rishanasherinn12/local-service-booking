from django import forms
from .models import Worker

class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['full_name','role','phone','email','experiance_years','location','photo','is_active']

        widgets = {
            "full_name":forms.TextInput(attrs={"class":"form-control"}),
            "role":forms.Select(attrs={"class":"form-control"}),
            "phone":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "experiance_years":forms.NumberInput(attrs={"class":"form-control"}),
            "location":forms.TextInput(attrs={"class":"form-control"}),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) != 10:
            raise forms.ValidationError("Phone no must must be exactly 10 digits")
        
        return phone
    
    def clean_experiance_years(self):
        exp = self.cleaned_data.get('experiance_years')
        
        if exp is not None and exp < 0:
            raise forms.ValidationError('Experience cannot be negative')
        return exp
