# accounts/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import CustomUser
from blog.models import Article


class ProfileView(LoginRequiredMixin, UpdateView):
    """نمایش و ویرایش پروفایل کاربر با کلاس بیس"""

    model = CustomUser
    fields = ['first_name', 'last_name', 'email', 'bio', 'avatar']
    template_name = 'profile.html'  # ← فقط profile.html بدون accounts/
    success_url = reverse_lazy('profile')  # ← profile بدون accounts:

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_articles = Article.objects.filter(author=self.request.user).order_by('-created_at')

        user_comments = []
        if hasattr(self.request.user, 'comments'):
            user_comments = self.request.user.comments.all().order_by('-created_at')[:10]

        context.update({
            'user_articles': user_articles,
            'articles_count': user_articles.count(),
            'published_count': user_articles.filter(status='published').count(),
            'draft_count': user_articles.filter(status='draft').count(),
            'user_comments': user_comments,
            'comments_count': user_comments.count() if user_comments else 0,
        })
        return context



    def form_valid(self, form):
        """هنگامی که فرم با موفقیت ذخیره شد"""
        messages.success(self.request, 'پروفایل شما با موفقیت به‌روزرسانی شد!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """هنگامی که فرم خطا داشت"""
        messages.error(self.request, 'خطایی رخ داد! لطفاً اطلاعات را بررسی کنید.')
        return super().form_invalid(form)