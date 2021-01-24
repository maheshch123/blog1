from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now
# Create your models here.

#######################
# for token
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

############

class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE,related_name='author')
    image = models.ImageField(blank=True, null=True, upload_to='post_pics')
    caption  = models.CharField(max_length=500)
    created_date = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return self.caption
    

    @property
    def number_of_comments(self):
        return Comment.objects.filter(post_connected=self).count()

    def get_absolute_url(self):
        return reverse('post_details', kwargs={'pk':self.pk})
        
############################################

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    address  = models.CharField(max_length=500)
    Dob = models.DateField(blank=True, null=True)
    cover_photos = models.ImageField(default='cover3.jpeg',upload_to='cover_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

###########################################

class Comment(models.Model):
    content = models.TextField(max_length=150)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_connected = models.ForeignKey(Post, on_delete=models.CASCADE)


    # def get_absolute_url(self):
    #     return reverse('post-detail', kwargs={'pk':self.pk})

# This code is triggered whenever a new user has been created and save the Token to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        