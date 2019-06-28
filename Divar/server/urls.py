from django.urls import path, include

from server.views.index import index
from server.views.signup import signup
from server.views.login import login
from server.views.post import post, load_subcategories, load_cluster
from server.views.test2 import test2
from server.views.user import user
from server.views.test import test

urlpatterns = [
    path('', index, name='index'),
    path('test/', test, name='test'),
    path('accounts/', include('django.contrib.auth.urls')),  # new
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('post/', post, name='post'),
    path('user/', user, name='user'),

    path('auth/', include('social_django.urls', namespace='social')),  # <- Here

    path('ajax/load-subcategories/', load_subcategories, name='ajax_load_subcategories'),
    path('ajax/load-cluster/', load_cluster, name='ajax_load_cluster'),

    path('test2/', test2, name='test2'),
]
