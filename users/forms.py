from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError
from .models import Profile
from django.contrib.auth import authenticate


MyUser = get_user_model()


class SignupForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'First name',
        }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Last name',
        }))
    email = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Email address',
        }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
        }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat password',
        }))
    
    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name','email','password1','password2')
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_email = MyUser.objects.filter(email=email)
        if user_email.exists():
            raise ValidationError("User with this email already exists")
        return email


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name')


class ChangeUserProfile(forms.ModelForm):
    profile_picture = forms.ImageField(required=False,
        widget=forms.FileInput(attrs={'id': 'profile_picture'}), error_messages={'invalid':('Image files only')})

    class Meta:
        model = Profile
        fields = ('profile_picture', 'status', 'description')


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(
        render_value=False, attrs={"class": "form-control", 
        "type": "password", "placeholder": "Enter old password"}))
    new_password = forms.CharField(label="New password", widget=forms.PasswordInput(
        render_value=False, attrs={"class": "form-control", 
        "type": "password", "placeholder": "New password"}))


