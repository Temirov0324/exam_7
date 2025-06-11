from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('article', 'reviewer', 'created_at')
    search_fields = ('article__title', 'reviewer__email', 'feedback')
    list_filter = ('created_at',)
    ordering = ('-created_at',)