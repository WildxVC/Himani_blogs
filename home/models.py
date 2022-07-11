from django.db import models
from django import forms
from django.contrib.auth.models import User
# from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE
from django.urls import reverse
from django.utils.text import slugify
import string
import random
from django.conf import settings
from django.contrib.auth import get_user_model


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

class Category(models.Model):
    cat_id = models.BigAutoField(primary_key = True)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=250, unique=True, editable = False)
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + "-" + self.title)
        super(Category, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("home:categories", args=[self.id, self.slug])


class Post(models.Model):
    post_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255,unique=True)
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user))
    desc = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now = True)
    views = models.IntegerField(null = True, blank = True, default = 0)
    img = models.FileField(upload_to= 'images', blank = False)
    slug = models.SlugField(max_length=250, unique=True, editable= False)
    
   
    def __str__(self):
        return self.cat_id.title + " | " + self.title + " |  by " + str(self.user)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + "-" + self.title)
        super(Post, self).save(*args, **kwargs)
        
    
