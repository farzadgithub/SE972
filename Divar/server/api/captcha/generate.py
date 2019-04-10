import base64
import io
import random

from server.models.Captcha import Captcha
from .image import image

suffix = ['یک',
          'دو',
          'سه',
          'چهار',
          'پنج',
          'شش',
          'هفت',
          'هشت',
          'نه',
          'ده',
          'یازده',
          'دوازده',
          ]

prefix = ['مدیر',
          'طراح',
          'بازیگر',
          'کارگردان',
          'عکاس',
          'پزشک',
          'دکتر',
          'مهندس',
          'کاردان',
          ]


def generate(ip):
    captcha_ip = Captcha.objects.filter(captcha_ip=ip)
    captcha_text = suffix[random.randint(0, len(suffix) - 1)] + ' ' + prefix[random.randint(0, len(prefix) - 1)]
    if captcha_ip:
        captcha_ip.update(captcha_text=captcha_text)
    else:
        captcha_generate = Captcha(captcha_ip=ip, captcha_text=captcha_text)
        captcha_generate.save()

    buffer = io.BytesIO()
    image(captcha_text).save(buffer, format='jpeg')

    return base64.b64encode(buffer.getvalue()).decode('utf-8')
