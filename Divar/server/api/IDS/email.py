from smtplib import SMTPAuthenticationError

from django.core.mail import EmailMessage


EMAIL_MESSAGES = {'success 1': '1',
                  'success 2': '2',
                  'success 3': '2',
                  'success 4': '2',
                  'failure 1': '1',
                  'failure 2': '1',
                  'failure 3': '1',
                  'failure 4': '1',
                  }


def send_email(email, title):
    print(email, title)
    email = EmailMessage(title, EMAIL_MESSAGES[title], to=[email])
    try:
        email.send()
    except Exception:
        print("Error sending email")

