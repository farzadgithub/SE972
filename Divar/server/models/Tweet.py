import datetime
from django.db import models
from django import forms


class Tweet(models.Model):
    username = models.CharField(max_length=20)
    username_hash = models.CharField(max_length=32, default='7d97481b1fe66f4b51db90da7e794d9f')
    title = models.CharField(max_length=30)
    body = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    hashtags = models.CharField(max_length=300)


class TweetForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'عنوان توییت'}),
                            label='عنوان توییت',
                            required=True,
                            disabled=False,
                            help_text='')
    body = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'متن توییت'}),
                           label='متن توییت',
                           required=True,
                           disabled=False,
                           help_text='')
    hashtags = None
    username = None
    username_hash = '7d97481b1fe66f4b51db90da7e794d9x'

    class Meta:
        model = Tweet
        exclude = ('username', 'hashtags', 'date', 'username_hash')

    def is_valid(self):
        self.full_clean()
        return self.data['title'] and self.data['body']
