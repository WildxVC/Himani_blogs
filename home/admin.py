from django.contrib import admin
from .models import Category, Post
from django.db import models
from tinymce.widgets import TinyMCE


admin.site.register(Category)



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
         js = [
            'tinymce/jquery.tinymce.min.js',
            'tinymce/tinymce.min.js',
            'TinyMce.js'
        ]
    formfield_overrides = {
         models.TextField: {'widget': TinyMCE()}
    }  

