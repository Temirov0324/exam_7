from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from articles.models import Edition, Article
from articles.serializers import EditionSerializer, ArticleSerializer
from .models import FAQ, Rule
from .serializers import FAQSerializer, RuleSerializer
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings


class MainPageView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        last_edition = Edition.objects.order_by('-created_at').first()
        last_approved_articles = Article.objects.filter(status='approved').order_by('-created_at')[:5]
        most_read_articles = Article.objects.order_by('-read_count')[:5]

        data = {
            'last_edition': EditionSerializer(last_edition,
                                              context={'request': request}).data if last_edition else None,
            'last_papers': ArticleSerializer(last_approved_articles, many=True, context={'request': request}).data,
            'most_read': ArticleSerializer(most_read_articles, many=True, context={'request': request}).data
        }
        return Response(data)


class FAQListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        faqs = FAQ.objects.all()
        serializer = FAQSerializer(faqs, many=True, context={'request': request})
        return Response(serializer.data)


class RuleListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        rules = Rule.objects.all()
        serializer = RuleSerializer(rules, many=True, context={'request': request})
        return Response(serializer.data)


class ContactView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        contact_info = {
            'address': _('Tashkent'),
            'telephone': _('online journal'),
            'email': _('journal.uz'),
        }
        return Response(contact_info)

    def post(self, request):
        first_name = request.data.get('first_name')
        email = request.data.get('email')
        message = request.data.get('message')

        if not all([first_name, email, message]):
            return Response({'error': _('All fields (first name, email, message) are required.')},
                            status=status.HTTP_400_BAD_REQUEST)


        subject = f'New message from {first_name}'
        message_body = f"Name: {first_name}\nEmail: {email}\nMessage: {message}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['tuit-bulletin@tuit.uz']

        try:
            send_mail(
                subject=subject,
                message=message_body,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            return Response({'message': _('Message sent successfully!')}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': _('Failed to send message. Try again later.')},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

