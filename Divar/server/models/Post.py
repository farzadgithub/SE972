import datetime
from xml import etree
from xml.etree import ElementTree

import requests
from django.db import models
from django import forms
from osm_field.fields import OSMField, LatitudeField, LongitudeField

from server.models.Category import Category, Subcategory, Cluster


class Post(models.Model):
    username = models.CharField(max_length=20)
    username_hash = models.CharField(max_length=32, default='7d97481b1fe66f4b51db90da7e794d9f')

    location = OSMField()
    location_lat = LatitudeField()
    location_lon = LongitudeField()

    title = models.CharField(max_length=30)

    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True)
    cluster = models.ForeignKey(Cluster, on_delete=models.SET_NULL, null=True)

    body = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)


class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'یک عنوان برای آگهی خود انتخاب کنید'}),
                            label='عنوان آگهی',
                            required=True,
                            disabled=False,
                            help_text='')
    body = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'متنی که می‌خواهید نمایش داده شود وارد کنید'}),
                           label='متن آگهی',
                           required=True,
                           disabled=False,
                           help_text='')
    search_keywords = None
    username = None
    username_hash = '7d97481b1fe66f4b51db90da7e794d9x'

    class Meta:
        model = Post
        # fields = ('category', 'subcategory', 'cluster')
        fields = (
            'category',
            'subcategory',
            'cluster',
            'location',
            'location_lat',
            'location_lon',
            'title',
            'body',
        )
        labels = {
            'category': 'انتخاب دسته',
            'subcategory': 'انتخاب زیردسته',
            'cluster': 'انتخاب طبقه‌بندی',
        }
        widgets = {
            'location': forms.HiddenInput(),
            'location_lat': forms.HiddenInput(),
            'location_lon': forms.HiddenInput(),
        }
        # exclude = ('username', 'search_keywords', 'date', 'username_hash')

    def is_valid(self):
        self.full_clean()
        valid = (self.data['title'] and self.data['body'] and self.data['category'] and self.data['subcategory'] and
                 self.data['cluster'] and self.data['location'] and self.data['location_lat'] and self.data[
                     'location_lon']) is not None
        if Cluster.objects.filter(category=self.data['category'], subcategory=self.data['subcategory'],
                                  id=self.data['cluster']) is None:
            valid = False

        try:
            lat = float(self.data['location_lat'])
            lng = float(self.data['location_lon'])
        except Exception:
            return False

        if valid and (not -90 < lat < 90 or not -90 < lng < 90):
            valid = False
        if valid:
            x = requests.get('https://nominatim.openstreetmap.org/reverse',
                             params={'format': 'json', 'lat': lat, 'lon': lng})

            print(x.json()['address']['neighbourhood'])

        return valid
