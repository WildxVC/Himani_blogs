from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Post

class AddPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['cat_id', 'title', 'img', 'desc']
