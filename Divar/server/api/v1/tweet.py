import json
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
from server.models import Userprofile, Tweet
from server.views.tweet import hashtag_extractor


@csrf_exempt
def tweet(request):
    try:
        data = json.loads(request.body)
        key = data['authentication_key']
        title = data['title']
        body = data['body']
        userprofile = Userprofile.objects.get(authentication_key=key)
        user = userprofile.user

        hashtags = hashtag_extractor(body)
        username = user.get_username()
        username_hash = hashlib.md5(username.encode('utf-8')).hexdigest()
        add_tweet = Tweet(username=username, username_hash=username_hash, title=title, body=body, date=timezone.now())
        add_tweet.save()
        return JsonResponse({'status': 'tweet added'})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'failed'})
