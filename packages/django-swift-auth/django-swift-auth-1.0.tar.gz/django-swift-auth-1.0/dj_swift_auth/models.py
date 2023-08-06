from datetime import date, datetime
from django.contrib.auth.models import AbstractUser
from django.db import models

from .manager import UserManager
from .utils import APPELLATION, GENDER


class User(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True, blank=True)
    phone_number = models.CharField(verbose_name='Phone Number', max_length=14, unique=True)
    appellation = models.IntegerField(choices=APPELLATION.get_choices(), default=APPELLATION.MEMBER.value)
    gender = models.IntegerField(choices=GENDER.select_gender(), default=GENDER.MALE.value)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(default=datetime.now)
    is_superuser = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile', blank=True, null=True)

    REQUIRED_FIELDS = ['email', 'phone_number']
    objects = UserManager()

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return str(self.username)

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def current_age(self):
        today = date.today()
        return (today - self.date_of_birth).days
