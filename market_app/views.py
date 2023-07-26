from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.views.generic import CreateView
from .forms import CreateUserForm, LoginForm


class LandingPageView(View):
    def get(self, request):
        context = {
            "logged_in": request.user.is_authenticated
        }

        return render(request, "base.html", context)


class LoginView(View):
    def get(self, request):
        form = LoginForm
        context = {"form": form}
        return render(request, "login.html", context)

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
        context = {"form": form}
        return render(request, "login.html", context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class CreateUserView(CreateView):
    form_class = CreateUserForm
    template_name = "user_creation_form.html"
    success_url = "/login/"

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            form.add_error('username', 'Login jest już zajęty.')

        password1 = form.cleaned_data.get('password1')
        password2 = form.cleaned_data.get('password2')
        if password1 != password2:
            form.add_error('password2', 'Hasła nie są takie same.')

        if form.is_valid():
            form.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
