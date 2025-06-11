from rest_framework import serializers
from .models import Notification
from users.serializers import UserSerializer
from articles.serializers import ArticleSerializer
from django.utils.translation import gettext_lazy as _

class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserSerializer(read_only=True)
    article = ArticleSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'recipient', 'article', 'message', 'is_read', 'created_at')

    def validate(self, data):
        if self.context['request'].user != data['recipient']:
            raise serializers.ValidationError({"error": _("Siz boshqa foydalanuvchilarning xabarnomalarini o‘zgartira olmaysiz")})
        return data