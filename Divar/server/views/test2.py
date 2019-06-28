from django.db import models
from django.shortcuts import render
from osm_field.fields import LatitudeField, LongitudeField, OSMField
from django import forms
from django.views.generic import CreateView


class MyModel(models.Model):
    location = OSMField()
    location_lat = LatitudeField()
    location_lon = LongitudeField()


class MyModelForm(forms.ModelForm):
    class Meta:
        fields = ('location', 'location_lat', 'location_lon',)
        model = MyModel

    location_lon = LongitudeField()


class MyCreateView(CreateView):
    form_class = MyModelForm
    model = MyModel


def test2(request):
    return render(request, 'test2.html', {'form': MyModelForm()})
