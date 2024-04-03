
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from .models import UserActivateToken
import logging
from django.utils import timezone

User = get_user_model()

logger = logging.getLogger('django')

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        print(instance,'----------')
        uat = UserActivateToken.generate_record(user=instance)
        logger.info("act_link:", uat.act_link)

        res = UserActivateToken.objects.filter(expired_at__lte = timezone.now())
        res.delete()
        
        send_mail(
            subject='Welcome to our society..',
            message='This is the test welcome message for you....!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
            html_message=f"""
			        <html><body>
                    <h3>Your Credentials for Login is....()</h3><br>
                    <h4>Email:{instance.email}</h4><br>
                    <h4>Email:{instance.password}</h4><br>
                    <a href="http://127.0.0.1:8000/verf-user/{uat.act_link}/">Please click here to activate your account!</a></body></html>
			        """
        )
