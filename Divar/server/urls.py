from django.urls import path, include

from server.views.index import index
from server.views.signup import signup
from server.views.login import login
from server.views.tweet import tweet
from server.views.user import user
from server.views.test import test
from server.api.v1.tweet import tweet as tweet_v1
from server.api.v1.login import login as login_v1
from server.api.v2.authentication import authentication as auth_v2

urlpatterns = [
    path('', index, name='index'),
    path('test/', test, name='test'),
    path('accounts/', include('django.contrib.auth.urls')),  # new
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('tweet/', tweet, name='tweet'),
    path('user/', user, name='user'),
    path('api/v1/login', login_v1, name='login_v1'),
    path('api/v1/tweet', tweet_v1, name='tweet_v1'),
    path('api/v2/auth', auth_v2, name='auth_v2'),

    path('auth/', include('social_django.urls', namespace='social')),  # <- Here
]
