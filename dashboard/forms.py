import requests
from django import forms
from django.contrib.auth.models import User

from dashboard.models import Beneficiary, Support, contactus


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    credit_amount = forms.IntegerField()
    narration = forms.CharField(max_length=100)
    email = forms.EmailField()
    username = forms.CharField(max_length=100)
    frommoney = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    checkboxed = forms.BooleanField()




class BeneficairyForm(forms.ModelForm):
    class Meta:
        model = Beneficiary
        fields = ['accountname', 'accountnumber', 'bankname',  ]


class supportForm(forms.ModelForm):
    class Meta:
        model = Support
        fields = ['title', 'description', 'affected_area',  ]


class contactusForm(forms.ModelForm):
    class Meta:
        model = contactus
        fields = ['reason', 'name', 'email', 'phonenumber', 'message',  ]

