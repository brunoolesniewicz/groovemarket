from django.db import models
from django.contrib.auth.models import AbstractUser
from autoslug import AutoSlugField


class CustomUser(AbstractUser):
    bio = models.TextField(max_length=150, blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='default_avatar.jpg', blank=False, null=True)
    follows = models.ManyToManyField('self', symmetrical=False, through="UsersFollows")

    def __str__(self):
        return self.username


class UsersFollows(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="following_users_set")
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="followers_users_set")
    date_of_follow = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower.username} follows {self.following.username} since {self.date_of_follow}'


class Listings(models.Model):
    CATEGORIES = (
        ("vinyl", "Winyl"),
        ("cd", "Płyta CD"),
        ("cassette", "Kaseta")
    )

    GENRES = (
        ("pop", "Pop"),
        ("rock", "Rock"),
        ("hip-hop/rap", "Hip-hip / Rap"),
        ("country", "Country"),
        ("r&b", "R&B"),
        ("edm", "EDM"),
        ("reggae", "Reggae"),
        ("classical", "Muzyka klasyczna"),
        ("metal", "Metal"),
        ("blues", "Blues"),
        ("indie", "Indie"),
        ("jazz", "Jazz"),
        ("other", "Inny")
    )

    CONDITIONS = (
        ("new", "Nowa"),
        ("perfect", "Idealny"),
        ("very good", "Bardzo dobry"),
        ("good", "Dobry"),
        ("acceptable", "Zadawalający"),
        ("poor", "Słaby")
    )

    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="seller")
    title = models.CharField(max_length=80, blank=False)
    description = models.TextField(max_length=200, blank=False)
    category = models.CharField(choices=CATEGORIES, blank=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=False)
    artist = models.CharField(max_length=30, blank=False)
    genre = models.CharField(choices=GENRES, blank=False)
    date_listed = models.DateTimeField(auto_now_add=True)
    condition = models.CharField(choices=CONDITIONS, blank=False)
    likes = models.ManyToManyField(CustomUser, blank=True, through="UsersLikes", related_name="liked_by")
    slug = AutoSlugField(populate_from="title", unique=True)
    sold = models.BooleanField(default=False, blank=False)
    image_1 = models.ImageField(upload_to=f'listing_images/', blank=True, null=True)
    image_2 = models.ImageField(upload_to=f'listing_images/', blank=True, null=True)
    image_3 = models.ImageField(upload_to=f'listing_images/', blank=True, null=True)

    def __str__(self):
        return self.title


class UsersLikes(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    liked_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.listing.title}"


class Conversations(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sender_user")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="receiver_user")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True, blank=True)
    last_message = models.ForeignKey('Messages', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name="conversation_last_message")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-last_message__sent_date']

    def __str__(self):
        return f"Conversation between {self.sender} and {self.receiver} about {self.listing}"


class Messages(models.Model):
    conversation = models.ForeignKey(Conversations, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    body = models.TextField(max_length=300)
    sent_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sent_date']

    def __str__(self):
        return f"{self.sender}: {self.body}"


class Offers(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    offer_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Offer for {self.listing.title} by {self.user.username}"
