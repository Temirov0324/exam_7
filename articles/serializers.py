from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Edition, Category, Tag, Article
from users.serializers import UserSerializer

class EditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edition
        fields = ('id', 'description', 'image', 'slug', 'created_at')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')

class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    edition = serializers.PrimaryKeyRelatedField(queryset=Edition.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Article
        fields = (
            'id', 'title', 'annotation', 'content', 'author', 'edition', 'category',
            'tags', 'image', 'status', 'read_count', 'created_at', 'updated_at'
        )

    def validate(self, data):
        if self.context['request'].user.role not in ['researcher', 'reviewer']:
            raise serializers.ValidationError({"role": _("Faqat tadqiqotchilar va ko‘rib chiqovchilar maqola yuklay oladi")})
        return data

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        tags = validated_data.pop('tags')
        article = Article.objects.create(**validated_data)
        article.tags.set(tags)
        return article