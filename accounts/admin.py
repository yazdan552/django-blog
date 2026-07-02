from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.


class CustomUserAdmin(UserAdmin):
    # فرم ویرایش کاربر موجود
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'email', 'bio')}),
        ('دسترسی‌ها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('تاریخ‌های مهم', {'fields': ('date_joined', 'last_login')}),
    )

    # فرم ایجاد کاربر جدید
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'bio'),
        }),
    )

    # نمایش ستون‌ها در لیست کاربران
    list_display = ('id','email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_display_links = ('email',)  # کلیک روی ایمیل برای ویرایش

    # فیلدهای جستجو و فیلتر
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    list_editable = ('is_active',)  # امکان فعال/غیرفعال کردن مستقیم از لیست

    # فیلدهای فقط خواندنی
    readonly_fields = ('date_joined', 'last_login')

    # مرتب‌سازی (جدیدترین اول)
    ordering = ('-date_joined',)


admin.site.register(CustomUser, CustomUserAdmin)