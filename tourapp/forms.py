from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import *

class VregistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['email','username','password1','password2']

class VloginForm(AuthenticationForm):
    pass

class CustregisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=['email','username','password1','password2']

class CloginForm(AuthenticationForm):
    pass


        
class PackageForm(forms.ModelForm):
    available_from=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}),input_formats=['%Y-%m-%d'],required=True)
    available_to=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}),input_formats=['%Y-%m-%d'],required=True)
    
    class Meta:
        model=TourPackages
        fields=['title','description','image','location','available_from','available_to','price']
        widgets={'description':forms.Textarea(attrs={'placeholder':'Enter detailed description'})}
        


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['no_of_people', 'phone_number', 'address']
        widgets = {
            'no_of_people': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of People','min': 1}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Full Address', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # get user from kwargs
        super(BookingForm, self).__init__(*args, **kwargs)

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if Booking.objects.filter(phone_number=phone).exclude(customer=self.user).exists():
            raise forms.ValidationError("This phone number is already used for another booking.")
        return phone