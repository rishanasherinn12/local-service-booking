from django import forms
from .models import Worker, Service

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
    

    
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title','category','description', 'includes', 'price', 'duration_minutes', 'image', 'is_active']

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control","placeholder": "AC Service & Repair"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control","placeholder": "0.00"}),
            "duration_minutes": forms.NumberInput(attrs={"class": "form-control","placeholder": "120"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4,"placeholder": "Describe what is included in this service..."}),
            "includes": forms.Textarea(attrs={"class": "form-control", "rows": 5,"placeholder": "Enter one item per line (e.g. Deep dusting, Floor cleaning, etc.)"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def clean_price(self):
        price = self.cleaned_data.get("price")

        if price < 50:
            raise forms.ValidationError("Minimum service price must be ₹50.")
        return price
    
    def clean_duration_minutes(self):
        duration = self.cleaned_data.get("duration_minutes")

        if duration <=0:
            raise forms.ValidationError("Duration must be greater than 0 minutes.")
        
        return duration