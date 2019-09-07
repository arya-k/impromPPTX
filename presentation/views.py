from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib import messages


class RegistrationView(View):
    template_name = 'register.html'
    form = UserCreationForm

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully registered!")
            return redirect('login')
        return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form()})


class LoginView(AuthLoginView):
    template_name = 'login.html'


class LogoutView(AuthLogoutView):
    template_name = 'logout.html'


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'present.html')
