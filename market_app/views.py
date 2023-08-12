from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser, Listings, UsersFollows, Offers, UsersLikes, Conversations, Messages
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import CreateUserForm, LoginForm, UpdateUserDetailsForm, CreateListingForm, CreateOfferForm, \
    CreateConversationForm, CreateMessageForm, ChangePasswordForm
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator
from django.db.models import Q


class LandingPageView(View):
    """
    LandingPageView: Wyświetla stronę główną z ofertami od obserwowanych użytkowników, jeśli jest się zalogowanym.
    W przeciwnym razie prosi o zalogowanie.
    """

    def get(self, request):
        user = request.user
        page = None

        if user.is_authenticated:
            following_users = UsersFollows.objects.filter(follower=user).values_list('following', flat=True)

            listings = Listings.objects.filter(seller__in=following_users).order_by('-date_listed')

            paginator = Paginator(listings, 10)
            page_number = request.GET.get('page')
            page = paginator.get_page(page_number)
        else:
            listings = None

        context = {
            "listings": listings,
            "page": page
        }
        return render(request, "base.html", context)


class LoginView(View):
    """
    LoginView: Wyświetla stronę logowania i obsługuje proces logowania użytkownika.
    """

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
    """
    LogoutView: Wylogowuje zalogowanego użytkownika.
    """

    def get(self, request):
        logout(request)
        return redirect("/")


class CreateUserView(CreateView):
    """
    CreateUserView: Obsługuje rejestrację użytkownika za pomocą formularza CreateUserForm.
    """

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
    """
    MyAccountView: Wyświetla szczegóły konta użytkownika oraz obsługuje usuwanie avatara.
    """

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

    def post(self, request):
        if "delete_avatar" in request.POST:
            user = request.user
            user.avatar = "default_avatar.jpg"
            user.save()
            messages.success(request, "Avatar został usunięty.")
        return redirect("/my_account/")


class UpdateUserDetailsView(LoginRequiredMixin, UpdateView):
    """
    UpdateUserDetailsView: Pozwala zalogowanemu użytkownikowi na aktualizację swoich danych.
    """

    form_class = UpdateUserDetailsForm
    template_name = "update_user_details_form.html"
    success_url = "/my_account/"

    def get_object(self, queryset=None):
        return self.request.user


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    """
    ChangePasswordView: Pozwala zalogowanemu użytkownikowi na zmianę hasła.
    """

    form_class = ChangePasswordForm
    template_name = "change_password_form.html"
    success_url = "/my_account/"


class UserListingsView(LoginRequiredMixin, View):
    """
    UserListingsView: Wyświetla oferty określonego użytkownika i obsługuje funkcje obserwowania/nieobserwowania
    oraz tworzenia rozmów.
    """

    def get(self, request, username):
        user = CustomUser.objects.get(username=username)
        listings = Listings.objects.filter(seller=user)
        followers_count = UsersFollows.objects.filter(following=user).count()
        following_count = UsersFollows.objects.filter(follower=user).count()
        user_followed = UsersFollows.objects.filter(follower=request.user, following=user).exists()
        conversation = Conversations.objects.filter(sender=request.user, receiver=user, listing=None)

        conversation_form = None
        if user.is_authenticated:
            initial_conversation_data = {
                'sender': request.user,
                'receiver': user,
                'listing': None
            }
            conversation_form = CreateConversationForm(initial=initial_conversation_data)

        context = {
            "listings": listings,
            "user": user,
            'user_listings_count': listings.count(),
            'followers_count': followers_count,
            'following_count': following_count,
            'user_followed': user_followed,
            'conversation_form': conversation_form,
            'conversation': conversation
        }

        return render(request, "user_listings.html", context)

    def post(self, request, username):
        user_to_follow = CustomUser.objects.get(username=username)
        user = request.user

        user_followed = UsersFollows.objects.filter(follower=user, following=user_to_follow).exists()

        if user_followed:
            UsersFollows.objects.filter(follower=user, following=user_to_follow).delete()
        else:
            UsersFollows.objects.create(follower=user, following=user_to_follow)

        form_conversation = CreateConversationForm(request.POST)
        if form_conversation.is_valid():
            conversation = form_conversation.save(commit=False)
            conversation.sender = user
            conversation.receiver = user_to_follow
            conversation.listing = None
            conversation.save()
            return redirect(f"/inbox/{conversation.id}")

        return redirect(f'/user/{user_to_follow.username}/')


class AllListingsView(LoginRequiredMixin, View):
    """
    AllListingsView: Wyświetla wszystkie oferty z opcjami wyszukiwania, filtrowania i sortowania.
    """

    def get(self, request):
        listings = Listings.objects.all().order_by('-date_listed')

        search_query = request.GET.get("q")
        if search_query:
            listings = listings.filter(Q(title__icontains=search_query) | Q(artist__icontains=search_query) | Q(
                seller__username__icontains=search_query))

        category_filter = request.GET.get('category')
        genre_filter = request.GET.get('genre')
        condition_filter = request.GET.get('condition')
        min_price_filter = request.GET.get('min_price')
        max_price_filter = request.GET.get('max_price')

        if category_filter:
            listings = listings.filter(category=category_filter)
        if genre_filter:
            listings = listings.filter(genre=genre_filter)
        if condition_filter:
            listings = listings.filter(condition=condition_filter)
        if min_price_filter:
            listings = listings.filter(price__gte=min_price_filter)
        if max_price_filter:
            listings = listings.filter(price__lte=max_price_filter)

        sort_option = request.GET.get('sort')
        if sort_option == 'newest':
            listings = listings.order_by('-date_listed')
        elif sort_option == 'oldest':
            listings = listings.order_by('date_listed')
        elif sort_option == 'cheapest':
            listings = listings.order_by('price')
        elif sort_option == 'expensive':
            listings = listings.order_by('-price')

        paginator = Paginator(listings, 10)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)

        context = {
            "listings": listings,
            "listings_count": Listings.objects.all().count(),
            "page": page,
            "categories": Listings.CATEGORIES,
            "genres": Listings.GENRES,
            "conditions": Listings.CONDITIONS
        }

        return render(request, "all_listings.html", context)


class ListingDetailsView(LoginRequiredMixin, View):
    """
    ListingDetailsView: Wyświetla szczegóły konkretnego ogłoszenia oraz obsługuje oferty, polubienia i rozmowy.
    """

    def get(self, request, slug):
        listing = Listings.objects.get(slug=slug)
        listing_likes_count = listing.likes.count()
        user = request.user
        is_liked = UsersLikes.objects.filter(user=user, listing_id=listing.id).exists()
        images_list = []
        conversation = Conversations.objects.filter(sender=user, receiver=listing.seller, listing=listing)

        if listing.image_1:
            images_list.append(listing.image_1)
        if listing.image_2:
            images_list.append(listing.image_2)
        if listing.image_3:
            images_list.append(listing.image_3)

        offer_form = None
        if user.is_authenticated and user != listing.seller:
            initial_offer_data = {
                'user': user,
                'listing': listing
            }
            offer_form = CreateOfferForm(initial=initial_offer_data)

        conversation_form = None
        if user.is_authenticated and user != listing.seller:
            initial_conversation_data = {
                'sender': user,
                'receiver': listing.seller,
                'listing': listing
            }
            conversation_form = CreateConversationForm(initial=initial_conversation_data)

        context = {
            "listing": listing,
            "images_list": images_list,
            "user": user,
            "offer_form": offer_form,
            "offers_count": Offers.objects.filter(listing_id=listing.id).count(),
            "is_liked": is_liked,
            "listing_likes_count": listing_likes_count,
            "conversation": conversation,
            "conversation_form": conversation_form
        }

        return render(request, "listing_details.html", context)

    def post(self, request, slug):
        listing = Listings.objects.get(slug=slug)
        user = request.user
        seller = listing.seller
        offer_form = None
        conversation_form = None

        if user.is_authenticated and user != listing.seller:
            form = CreateOfferForm(request.POST)
            if form.is_valid():
                offer = form.save(commit=False)
                offer.user = user
                offer.listing = listing
                offer.save()
                messages.success(request, "Oferta została wysłana!")

                return redirect(request.path_info)
            else:
                offer_form = form

            form_conversation = CreateConversationForm(request.POST)
            if form_conversation.is_valid():
                conversation = form_conversation.save(commit=False)
                conversation.sender = user
                conversation.receiver = seller
                conversation.listing = listing
                conversation.save()
                return redirect(f"/inbox/{conversation.id}")
            else:
                conversation_form = form_conversation

        context = {
            "listing": listing,
            "user": user,
            "offer_form": offer_form,
            "conversation_form": conversation_form
        }

        return render(request, "listing_details.html", context)


class UserFollowersView(LoginRequiredMixin, View):
    """
    UserFollowersView: Wyświetla listę obserwujących określonego użytkownika.
    """

    def get(self, request, username):
        user = CustomUser.objects.get(username=username)
        followers = UsersFollows.objects.filter(following=user)

        context = {
            "followers": followers
        }

        return render(request, "followers_list.html", context)


class UserFolloweringView(LoginRequiredMixin, View):
    """
    UserFolloweringView: Wyświetla listę użytkowników obserwowanych przez określonego użytkownika.
    """

    def get(self, request, username):
        user = CustomUser.objects.get(username=username)
        following = UsersFollows.objects.filter(follower=user)

        context = {
            "following": following
        }

        return render(request, "following_list.html", context)


class CreateListingView(LoginRequiredMixin, CreateView):
    """
    CreateListingView: Pozwala zalogowanemu użytkownikowi na dodanie nowego ogłoszenia.
    """

    form_class = CreateListingForm
    template_name = 'create_listing_form.html'
    model = Listings

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return f"/listing/{self.object.slug}"


class UpdateListingView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    UpdateListingView: Pozwala zalogowanemu użytkownikowi na aktualizację swojego ogłoszenia.
    """

    model = Listings
    form_class = CreateListingForm
    template_name = "edit_listing_form.html"

    def test_func(self):
        """
        Sprawdza czy zalogowany użytkownik jest właścicielem ogłoszenia.
        """
        listing = self.get_object()
        return self.request.user == listing.seller

    def get_success_url(self):
        return f"/listing/{self.object.slug}/"

    def form_valid(self, form):
        form.instance.slug = form.instance.title
        return super().form_valid(form)


class DeleteListingView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    DeleteListingView: Pozwala zalogowanemu użytkownikowi na usunięcie swojego ogłoszenia.
    """

    model = Listings
    template_name = "delete_listing_confirm.html"

    def test_func(self):
        """
        Sprawdza czy zalogowany użytkownik jest właścicielem ogłoszenia.
        """

        listing = self.get_object()
        return self.request.user == listing.seller

    def delete(self, request, *args, **kwargs):
        """
        Usuwanie ogłoszenia.
        """

        listing = Listings.objects.get(slug=self.kwargs['slug'])
        listing.delete()

        messages.success(request, "Ogłoszenie zostało pomyślnie usunięte.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return f"/user/{self.request.user.username}/"


class DeleteAccountView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    DeleteAccountView: Pozwala zalogowanemu użytkownikowi na usunięcie swojego konta.
    """

    model = CustomUser
    template_name = "delete_account_confirm.html"
    success_url = "/"

    def test_func(self):
        """
        Sprawdza czy zalogowany użytkownik jest właścicielem konta.
        """

        return self.request.user == self.get_object()

    def delete(self, request, *args, **kwargs):
        """
        Usuwanie konta.
        """
        user = self.request.user
        user.delete()

        messages.success(request, "Twoje konto zostało pomyślnie usunięte.")
        return super().delete(request, *args, **kwargs)


class UserOffersView(LoginRequiredMixin, View):
    """
    UserOffersView: Wyświetla oferty złożone na ogłoszenia użytkownika.
    """

    def get(self, request):
        user = request.user
        listings_with_offers = []

        for listing in Listings.objects.filter(seller=user):
            offers = Offers.objects.filter(listing=listing)
            listings_with_offers.append({
                'listing': listing,
                'offers': offers
            })

        context = {
            'listings_with_offers': listings_with_offers
        }

        return render(request, 'my_offers.html', context)


class DeleteOfferView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    DeleteOfferView: Pozwala zalogowanemu użytkownikowi na usunięcie niezadawalającej oferty.
    """

    model = Offers
    template_name = "delete_offer_confirm.html"
    success_url = "/my_offers/"

    def test_func(self):
        """
        Sprawdza czy zalogowany użytkownik jest właścicielem ogłoszenia, którego dotyczy oferta.
        """

        return self.request.user == self.get_object().listing.seller

    def delete(self, request, *args, **kwargs):
        """
        Usuwanie oferty.
        """

        offer = self.get_object()
        offer.delete()

        messages.success(request, "Oferta została usunięta.")
        return super().delete(request, *args, **kwargs)


class LikeView(LoginRequiredMixin, View):
    """
    LikeView: Obsługuje polubienie ogłoszenia.
    """

    def post(self, request, slug):
        listing = Listings.objects.get(slug=slug)
        user = request.user

        if not UsersLikes.objects.filter(user=user, listing=listing).exists():
            UsersLikes.objects.create(user=user, listing=listing)

        return redirect(request.META.get('HTTP_REFERER', '/'))


class UnlikeView(LoginRequiredMixin, View):
    """
    UnlikeView: Obsługuje usuwanie polubienia ogłoszenia.
    """

    def post(self, request, slug):
        listing = Listings.objects.get(slug=slug)
        user = request.user

        if UsersLikes.objects.filter(user=user, listing=listing).exists():
            UsersLikes.objects.filter(user=user, listing=listing).delete()

        return redirect(request.META.get('HTTP_REFERER', '/'))


class WishlistView(LoginRequiredMixin, View):
    """
    WishlistView: Wyświetla ogłoszenia polubione przez użytkownika.
    """

    def get(self, request):
        user = request.user
        user_likes = UsersLikes.objects.filter(user=user)
        liked_listings = [like.listing for like in user_likes]

        context = {
            "liked_listings": liked_listings
        }

        return render(request, "wishlist.html", context)


class ListingLikesView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    ListingLikesView: Wyświetla użytkowników, którzy polubili konkretne ogłoszenie.
    """

    def test_func(self):
        """
        Sprawdza czy zalogowany użytkownik jest właścicielem ogłoszenia, którego dotyczą polubienia.
        """

        listing = Listings.objects.get(slug=self.kwargs['slug'])
        return self.request.user == listing.seller

    def get(self, request, slug):
        listing = Listings.objects.get(slug=slug)
        likes = UsersLikes.objects.filter(listing=listing)

        context = {
            "listing": listing,
            "likes": likes
        }

        return render(request, "listing_likes.html", context)


class UserConversationView(LoginRequiredMixin, View):
    """
    UserConversationView: Wyświetla listę rozmów użytkownika.
    """

    def get(self, request):
        user = request.user
        user_conversations = Conversations.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-last_message')

        context = {
            "user": user,
            "sender": user_conversations[0].sender if user_conversations else None,
            "user_conversations": user_conversations
        }

        return render(request, "conversations_list.html", context)


class ConversationView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    ConversationView: Wyświetla i obsługuje wiadomości w ramach rozmowy.
    """

    def test_func(self):
        """
        Sprawdza czy zalogowany użytkownik jest uczestnikiem danej konwersacji.
        """

        conversation = Conversations.objects.get(id=self.kwargs['conversation_id'])
        return self.request.user == conversation.sender or self.request.user == conversation.receiver

    def get(self, request, conversation_id):
        user = request.user
        conversation = Conversations.objects.get(id=conversation_id)
        conversation_messages = Messages.objects.filter(conversation_id=conversation.id).order_by('sent_date')
        listing = None
        if conversation.listing:
            listing = conversation.listing

        initial_message_data = {
            'sender': user,
            'listing': listing,
            'conversation': conversation
        }
        message_form = CreateMessageForm(initial=initial_message_data)

        context = {
            "user": request.user,
            "conversation": conversation,
            "conversation_messages": conversation_messages,
            "listing": listing,
            "message_form": message_form
        }

        return render(request, "conversation.html", context)

    def post(self, request, conversation_id):
        user = request.user
        conversation = Conversations.objects.get(id=conversation_id)
        conversation_messages = Messages.objects.filter(conversation_id=conversation.id).order_by('sent_date')
        listing = None
        if conversation.listing:
            listing = conversation.listing

        form = CreateMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = user
            message.listing = listing
            message.save()

            conversation.last_message = message
            conversation.save()

            return redirect(request.path_info)
        else:
            message_form = form

        context = {
            'user': user,
            'listing': listing,
            'conversation': conversation,
            'message_form': message_form,
            'conversation_messages': conversation_messages
        }

        return render(request, "conversation.html", context)


class DeleteConversationView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    DeleteConversationView: Pozwala zalogowanemu użytkownikowi na usunięcie rozmowy.
    """

    model = Conversations
    template_name = "delete_conversation_confirm.html"
    success_url = "/inbox/"

    def test_func(self):
        """
        Sprawdza czy zalogowany użytkownik jest uczestnikiem danej konwersacji.
        """

        return self.request.user == self.get_object().sender or self.request.user == self.get_object().receiver

    def delete(self, request, *args, **kwargs):
        """
        Usuwanie konwersacji.
        """

        conversation = self.get_object()
        conversation.delete()

        messages.success(request, "Konwersacja została usunięta.")
        return super().delete(request, *args, **kwargs)
