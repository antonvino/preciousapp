from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from logs._mixins import TimestampsMixin
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils import timezone
from logs.services.logs_util import extract_tags


class UserManager(BaseUserManager):

    def create_user(self, email, username, password):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('The given e-mail must be set')
        email = self.normalize_email(email)
        user = self.model(username=username,
                          email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, username and password.
        """
        user = self.create_user(email=email, username=username, password=password)

        user.is_admin = True
        # user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    # def set_password(self, raw_password):
    #     self.password = make_password(raw_password)

    # def post_save(self, obj, created=False):
    #     """
    #     On creation, replace the raw password with a hashed version.
    #     """
    #     if created:
    #         obj.set_password(obj.password)
    #         obj.save()


class User(AbstractBaseUser, TimestampsMixin):
    # AUTHENTICATION
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(verbose_name="Is Active?", default=False,
                                    help_text="Unselect this instead of deleting accounts.")
    is_admin = models.BooleanField(verbose_name="Is Admin?", default=False,
                                   help_text="Select this to let users edit the website.")

    # DETAILS
    username = models.CharField(max_length=100, unique=True)

    date_joined=models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # (+ USERNAME_FIELD)

    def __unicode__(self):
        return self.full_name

    @property
    def full_name(self):
        return unicode(self.username)

    @property
    def short_name(self):
        return unicode(self.username)

    def get_short_name(self):
        return self.short_name

    @property
    def is_staff(self):
        return self.is_admin

    # cf. PermissionsMixin
    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the named permission.
        If obj is provided, the permission needs to be checked against a specific object instance.
        """
        return True

    def has_module_perms(self, app_label):
        """
        Returns True if the user has permission to access models in the given app.
        """
        return True


class Day(models.Model):
    # year = models.PositiveSmallIntegerField(default=0) # year-month-day are unique together
    # month = models.PositiveSmallIntegerField(default=0)
    # day = models.PositiveSmallIntegerField(default=0)
    date = models.DateField(auto_now_add=False, blank=False, null=False, verbose_name='Log date')
    day_text = models.CharField(max_length=2000, blank=True, null=True) # the day review - should be long as the field is long
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Date synced') # when the date review was synced with the web app
    author = models.ForeignKey('logs.User')

    class Meta:
        unique_together = ('date', 'author')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Day, self).save(force_insert, force_update, using, update_fields)
        """
        On creation, extract the tags from the day text
        """
        tags = extract_tags(self.day_text)

        for tag in tags:
            new_tag = Tag.objects.update_or_create(text=tag, author=self.author)

    def __unicode__(self):
        return u"Day {0}".format(self.date)
        # return u"Day {0}/{1}/{2}".format(self.day, self.month, self.year)


class Hour(models.Model):
    BAD = 0
    NEUTRAL = 1
    GOOD = 2
    PRODUCTIVE_CHOICES = ( # matches the SegmentedSelect in the MacOSX app
            (BAD, 'Bad'),
            (NEUTRAL, 'Neutral'),
            (GOOD, 'Good')
        )
    day = models.ForeignKey(Day) # foreign key to the day to make sure the day-hour is unique
    hour = models.PositiveSmallIntegerField(default=0)  
    productive = models.PositiveSmallIntegerField(choices=PRODUCTIVE_CHOICES, default=NEUTRAL)
    hour_text = models.CharField(max_length=300, blank=True, null=True) # the hour log text
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name = 'date synced') # when the hour log was synced with the web app
    author = models.ForeignKey('logs.User')

    class Meta:
        unique_together = ('day', 'hour', 'author')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Hour, self).save(force_insert, force_update, using, update_fields)
        """
        On creation, extract the tags from the hour text
        """
        tags = extract_tags(self.hour_text)

        for tag in tags:
            new_tag = Tag.objects.update_or_create(text=tag, author=self.author)

    def __unicode__(self):
        return u"Hour {0} {1}".format(self.day.date, self.hour)


class Tag(models.Model):
    text = models.CharField(max_length=300, blank=True, null=True)  # the hour log text
    author = models.ForeignKey('logs.User')

    class Meta:
        unique_together = ('text', 'author')

    def __unicode__(self):
        return u"Tag {0}".format(self.text)


class Download(models.Model):
    ip = models.GenericIPAddressField(blank=False, null=True, verbose_name="IP address")
    downloaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Date")

    def __unicode__(self):
        return u"Download {0} {1}".format(self.ip, self.downloaded_at)


# Automatically create token
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
