from django.contrib import admin
from .models import FAQ, Rule, Contact

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at', 'updated_at')
    search_fields = ('question', 'answer')
    ordering = ('-created_at',)

@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'created_at')
    search_fields = ('first_name', 'email', 'message')
    ordering = ('-created_at',)