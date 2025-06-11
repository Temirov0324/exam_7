from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'message', 'is_read', 'created_at')
    search_fields = ('recipient__email', 'message')
    list_filter = ('is_read', 'created_at')
    ordering = ('-created_at',)