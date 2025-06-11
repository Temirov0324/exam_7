from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid

class CustomUser(AbstractUser):
    USER_ROLES = (
        ('researcher', _('Researcher')),
        ('reviewer', _('Reviewer')),
        ('moderator', _('Moderator')),
    )
    role = models.CharField(max_length=20, choices=USER_ROLES, verbose_name=_('Role'))
    first_name = models.CharField(max_length=100, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=100, verbose_name=_('Last Name'))
    birth_date = models.DateField(null=True, blank=True, verbose_name=_('Birth Date'))
    email = models.EmailField(unique=True, verbose_name=_('Email'))
    organization = models.CharField(max_length=255, blank=True, verbose_name=_('Organization'))
    scientific_degree = models.CharField(max_length=255, blank=True, verbose_name=_('Scientific Degree'))
    image = models.ImageField(upload_to='user_images/', blank=True, null=True, verbose_name=_('Image'))
    position = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Position'))  # Reviewer uchun

    def __str__(self):
        return f"{self.username} - {self.role}"

    def save(self, *args, **kwargs):
        if self.role == 'moderator' and not self.pk:
            if CustomUser.objects.filter(role='moderator').count() >= 10:
                raise ValueError(_("Moderatorlar soni 10 tadan oshmasligi kerak."))
        super().save(*args, **kwargs)

    @classmethod
    def create_user(cls, **kwargs):
        password = kwargs.pop('password', None)
        user = cls(**kwargs)
        if password:
            user.set_password(password)
        user.save()
        return user

class PasswordResetCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_('User'))
    code = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name=_('Code'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    expires_at = models.DateTimeField(verbose_name=_('Expires At'))

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(minutes=30)
        super().save(*args, **kwargs)

    def is_valid(self):
        return timezone.now() <= self.expires_at