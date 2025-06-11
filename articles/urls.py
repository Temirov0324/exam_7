from django.urls import path
from . import views



urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('<int:pk>/assign-review/', views.AssignReviewView.as_view(), name='assign_review'),
]