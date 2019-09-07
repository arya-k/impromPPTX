from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
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
    next_page = "index"


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class ClickerView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'clicker.html')


class PresentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'present.html')


class GraphView(View):
    def get(self, request, *args, **kwargs):
        return redirect("http://cdn.pythagorasandthat.co.uk/wp-content/uploads/2014/07/quadratic-graph-1024x675.png")
