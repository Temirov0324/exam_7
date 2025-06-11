from django.db import models
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from publi.models import Publication

class Edition(models.Model):
    description = models.TextField(verbose_name=_('Description'))
    image = models.ImageField(upload_to='editions/', null=True, blank=True, verbose_name=_('Image'))
    slug = models.SlugField(unique=True, verbose_name=_('Slug'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    def __str__(self):
        return self.slug

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    slug = models.SlugField(unique=True, verbose_name=_('Slug'))

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    slug = models.SlugField(unique=True, verbose_name=_('Slug'))

    def __str__(self):
        return self.name

class Article(models.Model):
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('review', _('Under Review')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
    )
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    annotation = RichTextField(verbose_name=_('Annotation'))
    content = RichTextField(verbose_name=_('Content'))
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='articles', verbose_name=_('Author'))
    edition = models.ForeignKey(Edition, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Edition'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name=_('Category'))
    tags = models.ManyToManyField(Tag, verbose_name=_('Tags'))
    image = models.ImageField(upload_to='articles/', null=True, blank=True, verbose_name=_('Image'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name=_('Status'))
    read_count = models.IntegerField(default=0, verbose_name=_('Read Count'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    publication = models.ForeignKey(Publication, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Publication'))
    
    def __str__(self):
        return self.title