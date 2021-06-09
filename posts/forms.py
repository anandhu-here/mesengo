from django.conf import settings
from django import forms

from .models import Post

MAX_TWEET_LENGTH = 1000

class TweetForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
    
    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError("This tweet is too long")
        return content