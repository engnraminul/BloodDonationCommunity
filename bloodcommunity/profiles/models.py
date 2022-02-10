from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.db.models import Q


class ProfileManager(models.Manager):

    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        print(qs)
        print("#########")

        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
        print(accepted)
        print("#########")

        available = [profile for profile in profiles if profile not in accepted]
        print(available)
        print("#########")
        return available
        

    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles



class Profile(models.Model):

    BLOOD_GROUP_CHOICE = ( 
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    )

    DONATION_ACTIVITY = ( 
        ('Available', 'Available'),
        ('Unavailable', 'Unavailable'),
    
    )

    COUNTRY_CHOICE = ( 
        ('Bangladesh', 'Bangladesh'), 
    )

    DIVISION_CHOICE = ( 
        ('Barishal', 'Barishal'),
        ('Chittagong', 'Chittagong'),
        ('Dhaka', 'Dhaka'),
        ('Mymensingh ', 'Mymensingh'),
        ('Khulna', 'Khulna'),
        ('Rajshahi', 'Rajshahi'),
        ('Rangpur', 'Rangpur'),
        ('Sylhet', 'Sylhet'),
    )

    GENDER_CHOICE = ( 
        ('Famale', 'Famale'), 
        ('Male', 'Male'),
        ('3rd gender', '3rd gender'),
    )

    
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=200, blank=True, choices=GENDER_CHOICE)
    Blood_group_choice = models.CharField(max_length=11, choices = BLOOD_GROUP_CHOICE)
    donation_activity = models.CharField(max_length=50, choices = DONATION_ACTIVITY)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Last_date_of_donation = models.CharField(blank=True, max_length=300)
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=50, blank=True, choices= COUNTRY_CHOICE)
    Division = models.CharField(max_length=50, blank=True, choices= DIVISION_CHOICE)
    City = models.CharField(max_length=200, blank=True,)
    Area = models.CharField(max_length=200, blank=True,)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    objects = ProfileManager()



    def get_friends(self):
        return self.friends.all()
    
    def get_absolute_url(self):
        return reverse("profiles:profile-detail-view", kwargs={"slug": self.slug})

    def get_friends_no(self):
        return self.friends.all().count()

    def get_posts_no(self):
        return self.posts.all().count()

    def get_all_authors_posts(self):
        return self.posts.all()

    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value=='Like':
                total_liked += 1
        return total_liked

    def get_likes_recieved_no(self):
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"

    
    
    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name

    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug=="":
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)

STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)

class RelationshipManager(models.Manager):
    def invatations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs





class Relationship(models.Model):
    sender = models.name = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.name = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.name = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"