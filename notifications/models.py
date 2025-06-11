from django.db import models
from users.models import CustomUser
from articles.models import Article
from django.utils.translation import gettext_lazy as _

class Notification(models.Model):
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications', verbose_name=_('Recipient'))
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Article'))
    message = models.TextField(verbose_name=_('Message'))
    is_read = models.BooleanField(default=False, verbose_name=_('Is Read'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    def __str__(self):
        return f"{self.recipient.username} - {self.message}"