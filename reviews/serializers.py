from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from articles.models import Article
from .models import Review
from articles.serializers import ArticleSerializer
from users.serializers import UserSerializer

class ReviewSerializer(serializers.ModelSerializer):
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all())
    reviewer = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'reviewer', 'article', 'score', 'feedback', 'created_at')

    def validate(self, data):
        if self.context['request'].user.role != 'reviewer':
            raise serializers.ValidationError({"error": _("Faqat ko‘rib chiqovchilar sharh qoldira oladi")})
        if data['article'].author == self.context['request'].user:
            raise serializers.ValidationError({"error": _("Siz o‘zingizning maqolangizga sharh qoldira olmaysiz")})
        return data

    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user
        review = Review.objects.create(**validated_data)
        moderators = CustomUser.objects.filter(role='moderator')
        for moderator in moderators:
            Notification.objects.create(
                recipient=moderator,
                article=review.article,
                message=_("'{0}' maqolasiga yangi sharh qo‘shildi").format(review.article.title)
            )
        return review