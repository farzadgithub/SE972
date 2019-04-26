#from django.conf import settings
#from django.test import TestCase

from django.contrib.gis.geoip2 import GeoIP2
# Create your tests here.
#settings.configure()
GEOIP_PATH = "/geoip"
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
g = GeoIP2()
print(g.country_name('google.com'))
print(g.country('google.com'))