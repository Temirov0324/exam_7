from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('main/', views.MainPageView.as_view(), name='main_page'),
    path('faq/', views.FAQListView.as_view(), name='faq_list'),
    path('rules/', views.RuleListView.as_view(), name='rule_list'),
    path('contacts/', views.ContactView.as_view(), name='contact'),
]