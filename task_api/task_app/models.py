from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core import validators
import string
import random
import datetime
import logging
logger = logging.getLogger('django')

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, password2=None, **kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
           **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, password2=None, **kwargs):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            **kwargs
        )
        user.is_admin = True
        user.is_staff=True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    GENDER_CHOICES = [
                ('male', 'male'),
                ('female', 'female'),
                ('transgender', 'transgender')
        ]
    
    ROLE_CHOICES = [
                ('manager', 'manager'),
                ('team_leader', 'team_leader'),
                ('developer', 'developer')
        ]
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
   
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password =models.CharField(max_length=20)
    gender = models.CharField(max_length=50 ,choices=GENDER_CHOICES)
    profile = models.ImageField(upload_to="user/" ,blank=True, null=True, 
                   validators=[validators.FileExtensionValidator(allowed_extensions=['jpg','jpeg','png'])])  
    address = models.TextField()	
    pincode = models.IntegerField()
    city = models.CharField(max_length=20)
    contact_no = PhoneNumberField(blank=True, null=True)
    role = models.CharField(max_length =20 , choices=ROLE_CHOICES) 
    company = models.TextField()
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.role

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [ "username"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class UserActivateToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    act_link = models.CharField(max_length=32)
    created_at = models.DateTimeField()
    expired_at = models.DateTimeField()

    @staticmethod
    def generate_record(user):
        token = "".join(random.choices(string.ascii_letters + string.digits, k=32))
        curr_time = datetime.datetime.now()
        next_1hr = curr_time + datetime.timedelta(minutes=60)
        uat = UserActivateToken.objects.create(user=user, act_link=token, created_at=curr_time,
                                               expired_at=next_1hr)
        return uat

    def validate_user(self, token):
        try:
            curr_time = datetime.datetime.now()
            uats = UserActivateToken.objects.filter(act_link=token)

            for i in uats:
                if i.expired_at.timestamp() > curr_time.timestamp():
                    logger.info("-------error-----")
                    user = i.user
                    user.is_active = True
                    user.save()
                    i.delete()
                    logger.info("successfully deleted")
                    return True
                
                else:
                      i.delete()
                      return False
                
        except Exception as e:
            logger.exception("Exception at UserActivateToken --> validate_user():", e)
        return False


class Task(models.Model):
    TASK_CHOICES = [
        ("pending", "pending"),
        ("completed", "completed"),
        ("in_progress", "in_progress")
    ]
    task_id = models.IntegerField(primary_key=True) 
    task_name = models.CharField(max_length=200)
    task_description = models.TextField()
    task_status = models.CharField(max_length=30, choices= TASK_CHOICES)
    task_assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="manager_or_team_leader")
    task_assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="developer") 
    task_assigned_date = models.DateTimeField()
    task_completed_date = models.DateTimeField(blank=True, null=True)
    task_deadline =  models.DateTimeField()