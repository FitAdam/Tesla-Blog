from django import forms

from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'text', 'header_image']
        labels = {'title': '', 'text': '','header_image': '' }
       
