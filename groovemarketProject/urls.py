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
from django.conf import settings
from django.conf.urls.static import static
from market_app.views import LandingPageView, LoginView, LogoutView, CreateUserView, MyAccountView, \
    UpdateUserDetailsView, ChangePasswordView, UserListingsView, AllListingsView, ListingDetailsView, \
    UserFollowersView, UserFolloweringView

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
    path('user/<str:username>/', UserListingsView.as_view()),
    path('listing/<str:slug>/', ListingDetailsView.as_view()),
    path('user/<str:username>/followers/', UserFollowersView.as_view()),
    path('user/<str:username>/following/', UserFolloweringView.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
