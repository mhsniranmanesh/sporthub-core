import os
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
import uuid as uuid_lib
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from profiles.constants.profileConstants import Constants
from profiles.utils.profilePictureUtils import random_string_generator
from sporthub_core.celery import send_mail_async

class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    def user_profile_picture_path(self, filename):
        random_string = random_string_generator(size=5)
        final_file_name = ''.join([self.username, random_string])
        return 'profile_pictures/{0}.jpeg'.format(final_file_name)

    def user_avatar_path(self, filename):
        random_string = random_string_generator(size=5)
        final_file_name = ''.join([self.username, random_string])
        return 'profile_pictures/{0}-avatar.jpeg'.format(final_file_name)

    username = models.CharField(
        _('username'),
        max_length=50,
        unique=True,
        help_text=_('Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=50, blank=True)
    last_name = models.CharField(_('last name'), max_length=50, blank=True)
    email = models.EmailField(_('email address'), max_length=50, unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    phone_number = models.CharField(_('phone number'), max_length=16, blank=True)
    is_email_verified = models.BooleanField(_('email verified'), default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    title = models.CharField(_('title'), max_length=150, blank=True)
    bio = models.CharField(_('biograghy'), max_length=3000, blank=True)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True)
    balance = models.IntegerField(default=Constants.USER_INITIAL_BALANCE)
    rate = models.IntegerField(default=0)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return '%s' % (self.username)

    # def clean(self):
    #     super().clean()
    #     self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def send_verification_email(self, uid, token):
        plaintext = get_template('activate-email.txt')
        htmly = get_template('activate-email.html')
        d = {
            'user': self,
            'domain': 'wishwork.ir',
            'uid': uid,
            'token': token,
        }
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        subject = 'تایید ایمیل'
        from_email = 'mhsn.iranmanesh@gmail.com'
        to = self.email

        send_mail_async.delay(subject=subject, from_email=from_email, to_email=to, text_content=text_content,
                              html_content=html_content)

    def send_passwordreset_email(self, uid, token):
        plaintext = get_template('reset-password.txt')
        htmly = get_template('reset-password.html')
        d = {
            'user': self,
            'domain': 'wishwork.ir',
            'uid': uid,
            'token': token,
        }
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        subject = 'بازیابی رمز عبور'
        from_email = 'noreply@wishwork.ir'
        to = self.email

        send_mail_async.delay(subject=subject, from_email=from_email, to_email=to, text_content=text_content,
                              html_content=html_content)


@receiver(models.signals.post_delete, sender=User)
def auto_delete_profile_picture_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.profile_picture:
        if os.path.isfile(instance.profile_picture.path):
            os.remove(instance.profile_picture.path)

    return False


@receiver(models.signals.pre_save, sender=User)
def auto_delete_profile_picture_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        user = User.objects.get(pk=instance.pk)
        old_profile_pic = user.profile_picture
        old_avatar = user.avatar

        if old_profile_pic:
            new_profile_pic = instance.profile_picture

            if not old_profile_pic == new_profile_pic:
                if os.path.isfile(old_profile_pic.path):
                    os.remove(old_profile_pic.path)

        if old_avatar:
            new_avatar = instance.avatar

            if not old_avatar == new_avatar:
                if os.path.isfile(old_avatar.path):
                    os.remove(old_avatar.path)

        return False
    except User.DoesNotExist:
        return False

