from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Category, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ArticleForm, CommentForm
from django.urls import reverse_lazy
from django.db.models import Q


class ArticleListView(ListView):
    model = Article
    template_name = 'index.html'
    context_object_name = 'article_list'
    paginate_by = 5

    def get_queryset(self):
        queryset = Article.published.all()

        # جستجو
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()

        # فیلتر بر اساس دسته بندی
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('q', '')
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        return Article.objects.all()

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # افزایش بازدید
        obj.increase_views()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(is_active=True)
        context['comment_form'] = CommentForm()
        context['categories'] = Category.objects.all()
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_form.html'

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'مقاله با موفقیت منتشر شد!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'خطایی رخ داد! لطفاً فرم را دوباره بررسی کنید.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_form.html'

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'مقاله با موفقیت ویرایش شد!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'خطایی رخ داد! لطفاً فرم را دوباره بررسی کنید.')
        return super().form_invalid(form)

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_form_delete.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'مقاله با موفقیت حذف شد!')
        return super().delete(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, 'شما اجازه حذف این مقاله را ندارید!')
        return redirect('article_detail', slug=self.get_object().slug)


# ==================== ویو نظرات ====================

@login_required
def add_comment(request, slug):
    """اضافه کردن نظر جدید"""
    article = get_object_or_404(Article, slug=slug, status='published')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            messages.success(request, 'نظر شما با موفقیت ثبت شد!')
        else:
            messages.error(request, 'خطایی در ثبت نظر رخ داد!')

    return redirect('article_detail', slug=article.slug)


# ==================== ویو جستجو ====================

def search_articles(request):
    """جستجوی مقالات"""
    query = request.GET.get('q', '')
    articles = Article.published.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(tags__name__icontains=query)
    ).distinct() if query else Article.published.none()

    context = {
        'articles': articles,
        'query': query,
        'count': articles.count(),
    }
    return render(request, 'search_results.html', context)