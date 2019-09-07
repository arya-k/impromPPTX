from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib import messages
from django.http import HttpResponse

import random
import numpy as np
import tempfile
from matplotlib.figure import Figure


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
        plot_colors = ("#283593", "#2e7d32", "#a30000",
                       "#8e0038", "#009263", "#c4782e")
        line_colors = ("#ff3d00", "#00e676", "#2962ff",
                       "#ff1744", "#64dd17", "#9c27b0")

        num_elements = random.randint(300, 1000)
        x_range = random.uniform(1, 10) * (10 ** random.randint(-3, 4))
        y_range = random.uniform(1, 10) * (10 ** random.randint(-3, 4))

        xs = list(np.arange(0, x_range, x_range / num_elements))
        ys = [random.uniform(0, y_range)]
        for t in range(num_elements - 1):
            ys.append(ys[-1] + random.uniform(-y_range, y_range))

        xs, ys = zip(*zip(xs, ys))  # in case they aren't the same length
        z = np.polyfit(xs, ys, 3)
        f = np.poly1d(z)
        x_new = np.linspace(xs[0], xs[-1], 50)
        y_new = f(x_new)

        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)

        axis.plot(xs, ys, "o", ms=3, color=random.choice(plot_colors))
        axis.plot(x_new, y_new, color=random.choice(line_colors))
        tmpfile = tempfile.NamedTemporaryFile()
        fig.savefig(tmpfile.name + '.png')
        with open(tmpfile.name + '.png', 'rb') as f:
            return HttpResponse(f.read(), content_type='image/png')
