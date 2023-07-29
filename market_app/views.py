from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, Listings, UsersFollows
from django.views.generic import CreateView, UpdateView
from .forms import CreateUserForm, LoginForm, UpdateUserDetailsForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator


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


class MyAccountView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_listings_count = Listings.objects.filter(seller=user).count()
        followers_count = UsersFollows.objects.filter(following=user).count()
        following_count = UsersFollows.objects.filter(follower=user).count()

        context = {
            'user': user,
            'user_listings_count': user_listings_count,
            'followers_count': followers_count,
            'following_count': following_count,
        }

        return render(request, "my_account.html", context)


class UpdateUserDetailsView(LoginRequiredMixin, UpdateView):
    form_class = UpdateUserDetailsForm
    template_name = "update_user_details_form.html"
    success_url = "/my_account/"

    def get_object(self, queryset=None):
        return self.request.user


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "change_password_form.html"
    success_url = "/my_account/"


class UserListingsView(View):
    def get(self, request, username):
        user = CustomUser.objects.get(username=username)
        listings = Listings.objects.filter(seller=user)
        followers_count = UsersFollows.objects.filter(following=user).count()
        following_count = UsersFollows.objects.filter(follower=user).count()

        context = {
            "listings": listings,
            "user": user,
            'user_listings_count': listings.count(),
            'followers_count': followers_count,
            'following_count': following_count
        }

        return render(request, "user_listings.html", context)


class AllListingsView(View):
    def get(self, request):
        listings = Listings.objects.all()
        paginator = Paginator(listings, 10)

        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)

        context = {
            "listings": listings,
            "listings_count": listings.count(),
            "page": page
        }

        return render(request, "all_listings.html", context)


class ListingDetailsView(View):
    def get(self, request, slug):
        listing = Listings.objects.get(slug=slug)

        context = {
            "listing": listing
        }

        return render(request, "listing_details.html", context)


class UserFollowersView(View):
    def get(self, request, username):
        user = CustomUser.objects.get(username=username)
        followers = UsersFollows.objects.filter(following=user)

        context = {
            "followers": followers
        }

        return render(request, "followers_list.html", context)


class UserFolloweringView(View):
    def get(self, request, username):
        user = CustomUser.objects.get(username=username)
        following = UsersFollows.objects.filter(follower=user)

        context = {
            "following": following
        }

        return render(request, "following_list.html", context)
