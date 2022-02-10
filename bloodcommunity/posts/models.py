from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile

# Create your models here.



class Post(models.Model):
    BLOOD_CHOICE = ( 
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
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


    
    patient_Name = models.CharField(max_length=200, blank=True)
    Blood_group = models.CharField(max_length=10, choices = BLOOD_CHOICE)
    gender = models.CharField(max_length=200, blank=True, choices=GENDER_CHOICE)
    Ammount_of_blood= models.IntegerField(blank=True, null=True)
    patient_types = models.CharField(max_length=200, blank=True)
    donation_date = models.CharField(max_length=50, blank=True)
    donation_time = models.CharField(max_length=20, blank=True)
    Division = models.CharField(max_length=50, blank=True, choices= DIVISION_CHOICE)
    area = models.CharField(max_length=200, blank=True)
    hospital_name = models.CharField(max_length=200, blank=True)
    contact = models.CharField(max_length=50, blank=True)
    post_text = models.TextField()
    image = models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return str(self.post_text[:20])
    

    def num_likes(self):
        return self.liked.all().count()

    def num_comments(self):
        return self.comment_set.all().count()

    class Meta:
        ordering = ('-created',)

class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model): 
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"
