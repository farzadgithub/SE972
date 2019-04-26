import datetime
from django.db import models
from django import forms

from server.models.Category import Category, Subcategory


class Post(models.Model):
    username = models.CharField(max_length=20)
    username_hash = models.CharField(max_length=32, default='7d97481b1fe66f4b51db90da7e794d9f')

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    title = models.CharField(max_length=30)

    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True)


    body = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)


class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'عنوان آگهی'}),
                            label='عنوان آگهی',
                            required=True,
                            disabled=False,
                            help_text='')
    body = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'متن آگهی'}),
                           label='متن آگهی',
                           required=True,
                           disabled=False,
                           help_text='')
    search_keywords = None
    username = None
    username_hash = '7d97481b1fe66f4b51db90da7e794d9x'

    class Meta:
        model = Post
        fields = ('title', 'body', 'category', 'subcategory')
        labels = {
            'subcategory': 'زیردسته',
            'category': 'دسته‌بندی',
        }
        # exclude = ('username', 'search_keywords', 'date', 'username_hash')

    def is_valid(self):
        self.full_clean()
        return self.data['title'] and self.data['body']
