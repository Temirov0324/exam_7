from django.db import models
from users.models import CustomUser
from articles.models import Article
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

class Review(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='reviews', verbose_name=_('Article'))
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_('Reviewer'))
    score = models.IntegerField(choices=[(i, i) for i in range(1, 11)], verbose_name=_('Score'))
    feedback = RichTextField(verbose_name=_('Feedback'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    def __str__(self):
        return f"{self.reviewer.username} - {self.article.title}"