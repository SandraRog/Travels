from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# class LoginForm(forms.Form):
#
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)
#
#
# class UserCreateForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}))
#
#     class Meta:
#         model = User
#         fields = ['username']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs.update({'placeholder': 'email'})
#
#     def clean(self):
#         data = super().clean()
#         password = data['password']
#         password2 = data['password2']
#         if password != password2:
#             raise ValidationError('Passwords must be the same')
#         return data
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])
#         if commit:
#             user.save()
#         return user

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30, label='First Name', widget=forms.TextInput)
    last_name = forms.CharField(max_length=30, label='Last Name', widget=forms.TextInput)
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords must match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Ustawianie username na email
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

