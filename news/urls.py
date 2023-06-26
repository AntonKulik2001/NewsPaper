from django.urls import path
from .views import *

urlpatterns = [
    path('', NewsList.as_view(), name='News_list'),
    path('<int:pk>', Textnews.as_view(), name='Text_news'),
    path('news/create/', CreateNews.as_view(), name='News_create'),
    path('news/<int:pk>/edit/', UpdateNews.as_view(), name='News_update'),
    path('news/<int:pk>/delete/', DeleteNews.as_view(), name='News_delete'),
    path('articles/create/', ArticlesCreate.as_view(), name='Articles_create'),
    path('articles/<int:pk>/edit', UpdateArticles.as_view(), name='Articles_update'),
    path('articles/<int:pk>/delete', DeleteArticles.as_view(), name='Articles_delete'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
]