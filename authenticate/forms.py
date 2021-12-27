from django.forms import ModelForm, Form
from django.contrib.auth.forms import UserCreationForm
from django import forms
from authenticate.models import users
from django.contrib.auth.models import User
import datetime


# Create the form class.

class UserRegisterForm(ModelForm, forms.Form):
    class Meta:
        model = users
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.SelectDateWidget(years=range(2015, 1900, -1)),
            'create_password': forms.PasswordInput,
            'confirm_password': forms.PasswordInput
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Username aldready exists')
        return username

    def clean_date_of_birth(self):
        userAge = 13
        dob = self.cleaned_data.get('date_of_birth')
        today = datetime.date.today()
        if (dob.year + userAge, dob.month, dob.day) > (today.year, today.month, today.day):
            raise forms.ValidationError('User must be aged {} years and above.'. format(userAge))
        return dob

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'A user has already registered using this email')
        return email

    def clean_password(self):
        '''
        we must ensure that both passwords are identical
        '''
        password1 = self.cleaned_data.get('creat_password')
        password2 = self.cleaned_data.get('confirm_password')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords must match')
        return password2

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return first_name

    def clean_contact(self):
        contact = self.cleaned_data.get('contact_number')
        if len(contact) < 10:
            raise forms.ValidationError('Enter a valid contact number')
        return contact
