from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from shortuuid.django_fields import ShortUUIDField
import uuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


from .managers import UserManager

STUDENT_STATUS = (
    ("active", "Active"),
    ("in-active", "In-Active")
)


class MyUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email Address...'), unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    other_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    username = models.CharField(max_length=150, unique=True, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_staff = models.BooleanField(_('is staff'), default=False)
    is_admin = models.BooleanField(_('is admin'), default=False)
    is_active = models.BooleanField(_('is active'), default=True)



    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'other_name', 'last_name', 'username']

    
    
    def __str__(self):
        return self.username


    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
    def get_full_name(self):
        """
            This Function returns the First name and the last name together with a space inbetween
        """
        full_name = '%s %s %s' % (self.first_name, self.other_name, self.last_name)
        return full_name.strip()
        
    def get_short_name(self):
        """
            returns the shortname for the user
        """
        return self.first_name
        
        
    def email_user(self, subject, message, from_email=None, **kwargs):
        """
            Sends an email to the user
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


#Profile models For Creating a model for users
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bio = models.TextField()
    location = models.CharField(max_length=300, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='defaultpic.jpg', null=True, blank=True)
    created = models.DateTimeField(auto_now=True)
    updated =  models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.user.get_full_name()
    
    
#A Function that creates a Profile immediately a user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_model(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        


class MatricNumber(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='matriculation_number')
    matric_number = ShortUUIDField(length=6, max_length=5, prefix='IIC24', alphabet="1234567890", unique=True)
    student_status = models.CharField(max_length=100, choices=STUDENT_STATUS, default="in-active")
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.get_full_name()


# Add a signal receiver function to create a MatricNumber instance when a MyUser instance is created
@receiver(post_save, sender=MyUser)
def create_matric_number(sender, instance, created, **kwargs):
    if created:
        MatricNumber.objects.create(user=instance)

# Add a signal receiver function to save the MatricNumber instance when the MyUser instance is saved
@receiver(post_save, sender=MyUser)
def save_matric_number(sender, instance, **kwargs):
    instance.matriculation_number.save()

