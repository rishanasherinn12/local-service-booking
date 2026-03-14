import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomerProfile, Address


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required = True)
    phone = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken")

        return username

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit() or len(phone) !=10:
            raise forms.ValidationError("Enter a valid 10 digits phone number")
        return phone
        
    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
            


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['full_name','phone']

    def clean_full_name(self):
        name = self.cleaned_data['full_name'].strip()

        if len(name)<3:
            raise forms.ValidationError("Full name must be at least 3 characters.")
        
        if not re.match(r'^[A-Za-z\s]+$',name):
            raise forms.ValidationError("Name can contain only letters and spaces.")
        return name
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if not phone.isdigit():
            raise forms.ValidationError("Phone must contain only digits")

        if len(phone) != 10:
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        return phone



class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['label','full_address','city','state','pincode','landmark','is_default']

    def clean_pincode(self):
        pincode = self.cleaned_data['pincode']
        if not pincode.isdigit():
            raise forms.ValidationError("Pincode must contain only digits")
        
        if len(pincode) !=6:
            raise forms.ValidationError("Enter a valid 6 digit pincode")
        return pincode

    def clean_city(self):
        city = self.cleaned_data['city']

        if not re.match(r'^[A-Za-z\s]+$', city):
            raise forms.ValidationError("City can contain only letters")

        return city


    def clean_state(self):
        state = self.cleaned_data['state']

        if not re.match(r'^[A-Za-z\s]+$', state):
            raise forms.ValidationError("State can contain only letters")

        return state

    def clean_full_address(self):
        address = self.cleaned_data['full_address'].strip()

        if len(address) < 10:
            raise forms.ValidationError("Address must be at least 10 characters long")

        return address
    
    def clean_label(self):
        label = self.cleaned_data['label'].strip()

        if len(label) < 2:
            raise forms.ValidationError("Label must contain at least 2 characters")

        return label