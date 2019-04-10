from server.models.Captcha import Captcha


def validate(ip, text):
    if Captcha.objects.filter(captcha_ip=ip, captcha_text=text):
        Captcha.objects.filter(captcha_ip=ip, captcha_text=text).delete()
        return True
    return False
