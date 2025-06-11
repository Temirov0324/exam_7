from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Article
from .serializers import ArticleSerializer
from notifications.models import Notification
from users.models import CustomUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ArticleListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status', 'author']
    search_fields = ['title', 'content']
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(
        operation_description="Barcha maqolalarni olish, filtr, qidiruv va sahifalash bilan",
        responses={200: ArticleSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter('status', openapi.IN_QUERY, description="Maqola holati", type=openapi.TYPE_STRING),
            openapi.Parameter('author', openapi.IN_QUERY, description="Maqola muallifi", type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description="Maqola sarlavhasi yoki matnida qidirish", type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description="Sahifa raqami", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Har bir sahifadagi elementlar soni", type=openapi.TYPE_INTEGER),
        ]
    )
    def get(self, request):
        articles = Article.objects.all()
        # Filtrlash
        if self.filterset_fields:
            for field in self.filterset_fields:
                value = request.query_params.get(field)
                if value:
                    articles = articles.filter(**{field: value})
        # Qidiruv
        search_query = request.query_params.get('search')
        if search_query:
            articles = articles.filter(title__icontains=search_query) | articles.filter(content__icontains=search_query)
        
        # Sahifalash
        paginator = self.pagination_class()
        paginated_articles = paginator.paginate_queryset(articles, request)
        serializer = ArticleSerializer(paginated_articles, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_description="Yangi maqola yaratish",
        request_body=ArticleSerializer,
        responses={201: ArticleSerializer, 400: "Yaroqsiz so'rov"}
    )
    def post(self, request):
        serializer = ArticleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            article = serializer.save()
            moderators = CustomUser.objects.filter(role='moderator')
            for moderator in moderators:
                Notification.objects.create(
                    recipient=moderator,
                    article=article,
                    message=_("Yangi maqola yuklandi: {0}").format(article.title)
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
            article.read_count += 1
            article.save()
            serializer = ArticleSerializer(article, context={'request': request})
            return Response(serializer.data)
        except Article.DoesNotExist:
            return Response({"error": _("Maqola topilmadi")}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
            if request.user.role != 'moderator':
                return Response({"error": _("Faqat moderatorlar maqolani tahrirlay oladi")}, status=status.HTTP_403_FORBIDDEN)
            serializer = ArticleSerializer(article, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                article = serializer.save()
                Notification.objects.create(
                    recipient=article.author,
                    article=article,
                    message=_("Sizning maqolangiz '{0}' holati {1} ga o‘zgartirildi").format(article.title, article.status)
                )
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Article.DoesNotExist:
            return Response({"error": _("Maqola topilmadi")}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
            if request.user.role != 'moderator':
                return Response({"error": _("Faqat moderatorlar maqolani o‘chira oladi")}, status=status.HTTP_403_FORBIDDEN)
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Article.DoesNotExist:
            return Response({"error": _("Maqola topilmadi")}, status=status.HTTP_404_NOT_FOUND)

class AssignReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
            if request.user.role != 'moderator':
                return Response({"error": _("Faqat moderatorlar maqolani ko‘rib chiqish uchun tayinlay oladi")}, status=status.HTTP_403_FORBIDDEN)
            article.status = 'review'
            article.save()
            reviewers = CustomUser.objects.filter(role='reviewer')
            for reviewer in reviewers:
                Notification.objects.create(
                    recipient=reviewer,
                    article=article,
                    message=_("Sizga ko‘rib chiqish uchun '{0}' maqolasi tayinlandi").format(article.title)
                )
            serializer = ArticleSerializer(article, context={'request': request})
            return Response(serializer.data)
        except Article.DoesNotExist:
            return Response({"error": _("Maqola topilmadi")}, status=status.HTTP_404_NOT_FOUND)
        

