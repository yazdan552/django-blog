from django.urls import path, re_path
from .views import (
    ArticleListView, ArticleDetailView, ArticleCreateView,
    ArticleUpdateView, ArticleDeleteView, add_comment, search_articles
)

urlpatterns = [
    path('', ArticleListView.as_view(), name='index'),

    # آدرس‌های خاص باید اول بیایند
    path('article/new', ArticleCreateView.as_view(), name='article_create'),
    re_path(r'^article/(?P<slug>.+)/update/$', ArticleUpdateView.as_view(), name='article_update'),
    re_path(r'^article/(?P<slug>.+)/delete/$', ArticleDeleteView.as_view(), name='article_delete'),
    re_path(r'^article/(?P<slug>.+)/comment/$', add_comment, name='add_comment'),

    # آدرس عمومی article_detail باید آخر بیاید
    re_path(r'^article/(?P<slug>.+)/$', ArticleDetailView.as_view(), name='article_detail'),

    # جستجو
    path('search/', search_articles, name='search'),
]