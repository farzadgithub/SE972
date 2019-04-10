from smtplib import SMTPAuthenticationError

from django.core.mail import EmailMessage


EMAIL_MESSAGES = {'success': 'با سلام. یک ورود موفق به سامانه server داشتید.',
                  'failure': 'با سلام. یک ورود ناموفق به سامانه server داشتید.'}


def send_email(email, title):
    print(email, title)
    email = EmailMessage(title, EMAIL_MESSAGES[title], to=[email])
    try:
        email.send()
    except Exception:
        print("Error sending email")

