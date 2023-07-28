"""
URL configuration for groovemarketProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from market_app.views import LandingPageView, LoginView, LogoutView, CreateUserView, MyAccountView, \
    UpdateUserDetailsView, ChangePasswordView, UserListingsView, AllListingsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('register/', CreateUserView.as_view()),
    path('my_account/', MyAccountView.as_view()),
    path('my_account/edit/', UpdateUserDetailsView.as_view()),
    path('my_account/password/', ChangePasswordView.as_view()),
    path('all_listings/', AllListingsView.as_view()),
    path('<str:username>/', UserListingsView.as_view())
]
