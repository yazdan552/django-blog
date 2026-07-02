from django.db import models
from django.conf import settings
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.urls import reverse


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام دسته بندی")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="آدرس دسته", allow_unicode=True)
    description = models.TextField(blank=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Article(models.Model):
    STATUS_CHOICES = (
        ('draft', 'پیش‌نویس'),
        ('published', 'منتشر شده'),
    )

    title = models.CharField(max_length=200, verbose_name="عنوان")
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, blank=True, verbose_name="آدرس مقاله")
    content = models.TextField(verbose_name="محتوای مقاله")
    image = models.ImageField(upload_to='articles/%Y/%m/%d/', blank=True, null=True, verbose_name="تصویر")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles',
                                 verbose_name='دسته بندی')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles',
                               verbose_name='نویسنده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ انتشار")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='وضعیت')
    tags = TaggableManager(blank=True, verbose_name="تگ‌ها")

    # فیلدهای جدید برای آمار
    views_count = models.PositiveIntegerField('تعداد بازدید', default=0)
    comments_count = models.PositiveIntegerField('تعداد نظرات', default=0)

    # Managers
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.slug])

    def increase_views(self):
        """افزایش تعداد بازدید مقاله"""
        self.views_count += 1
        self.save(update_fields=['views_count'])

    @property
    def reading_time(self):
        """محاسبه زمان تقریبی مطالعه (بر اساس 200 کلمه در دقیقه)"""
        word_count = len(self.content.split())
        minutes = max(1, word_count // 200)
        return minutes


class Comment(models.Model):
    """مدل نظرات برای مقالات"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='مقاله')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments',
                               verbose_name='نویسنده')
    text = models.TextField('متن نظر', max_length=1000)
    created_at = models.DateTimeField('تاریخ نظر', auto_now_add=True)
    is_active = models.BooleanField('وضعیت', default=True)

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author} - {self.article.title}'

    def save(self, *args, **kwargs):
        """هنگام ذخیره نظر، تعداد نظرات مقاله را به‌روز می‌کند"""
        super().save(*args, **kwargs)
        self.article.comments_count = self.article.comments.filter(is_active=True).count()
        self.article.save(update_fields=['comments_count'])