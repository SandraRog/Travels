from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views import View
from accounts.forms import LoginForm, UserCreateForm


# Create your views here.

class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            print(user)
            if user is not None:
               login(request, user)
               # print(request.user)
               next_url = request.GET.get('next', 'index')
               return redirect(next_url)
            form = LoginForm()
        return render(request, 'login.html', {'form': form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('base')


class UserCreateView(View):
    def get(self, request):
        form = UserCreateForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Po pomyślnej rejestracji przekieruj na stronę logowania
        return render(request, 'register.html', {'form': form})