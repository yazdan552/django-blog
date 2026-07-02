from django.contrib import admin
from .models import Category, Article


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug','description')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'author', 'status', 'created_at')
    list_display_links = ('title',)  # کلیک روی عنوان برای ویرایش
    list_filter = ('status', 'created_at', 'author', 'category')
    list_editable = ('status',)  # تغییر وضعیت مستقیم از لیست
    search_fields = ('title', 'content')
    raw_id_fields = ('author',)
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
    tag_list.short_description = 'برچسب‌ها'

    list_display = list(list_display) + ['tag_list']