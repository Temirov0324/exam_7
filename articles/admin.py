from django.contrib import admin
from .models import Article, Edition, Category, Tag

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'read_count', 'created_at')
    search_fields = ('title', 'author__email', 'annotation')
    list_filter = ('status', 'category', 'created_at')
    ordering = ('-created_at',)

@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')  # 'publication_date' va 'number' o'rniga 'id' va 'created_at' ishlatildi
    search_fields = ('id',)  # 'publication_date' o'rniga 'id' ishlatildi
    ordering = ('-created_at',)  # 'publication_date' o'rniga 'created_at' ishlatildi

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')  # 'created_at' olib tashlandi
    search_fields = ('name', 'slug')
    ordering = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')  # 'created_at' olib tashlandi
    search_fields = ('name', 'slug')
    ordering = ('name',)