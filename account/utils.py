from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings

from .tokens import account_activation_token

def send_verification_mail(user, current_site, email):
    mail_subject = 'Verify email'
    message = render_to_string('account/email_templates/email_template.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        })
    try:
        number = send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
    except:
        return False

    if number:
        return True 
    
    return False