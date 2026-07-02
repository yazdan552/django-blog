# blog/forms.py

from django import forms
from .models import Article, Comment
from PIL import Image  # اضافه کنید


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'image', 'tags', 'status']

        labels = {
            'title': 'عنوان مقاله',
            'content': 'محتوای مقاله',
            'category': 'دسته بندی',
            'image': 'تصویر شاخص',
            'tags': 'برچسب‌ها',
            'status': 'وضعیت انتشار',
        }

        help_texts = {
            'image': 'فرمت‌های مجاز: JPG, PNG, WEBP (حداکثر ۲ مگابایت)',
            'tags': 'برچسب‌ها را با کاما جدا کنید (مثال: جنگو، پایتون، طراحی وب)',
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان جذاب و کوتاه انتخاب کنید'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 12,
                'placeholder': 'محتوای مقاله خود را بنویسید...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png,image/webp'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: جنگو، پایتون، برنامه نویسی'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    # اعتبارسنجی عنوان (تکراری نباشد)
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Article.objects.filter(title=title).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('این عنوان قبلاً استفاده شده است! لطفاً عنوان دیگری انتخاب کنید.')
        return title

    # اعتبارسنجی عکس - روش صحیح
    def clean_image(self):
        image = self.cleaned_data.get('image')

        # اگر تصویری آپلود نشده یا در حال ویرایش است و تصویر تغییر نکرده
        if not image:
            return image

        # بررسی حجم فایل (حداکثر 2 مگابایت)
        if image.size > 2 * 1024 * 1024:
            raise forms.ValidationError('حجم فایل نباید بیشتر از ۲ مگابایت باشد!')

        # بررسی فرمت فایل با استفاده از نام فایل
        allowed_extensions = ['jpg', 'jpeg', 'png', 'webp']
        file_extension = image.name.split('.')[-1].lower()

        if file_extension not in allowed_extensions:
            raise forms.ValidationError('فرمت فایل باید JPG, JPEG, PNG یا WEBP باشد!')

        # بررسی محتوای واقعی فایل (اختیاری)
        try:
            img = Image.open(image)
            img.verify()  # بررسی اینکه واقعاً تصویر است
        except Exception:
            raise forms.ValidationError('فایل آپلود شده یک تصویر معتبر نیست!')

        return image


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'نظر خود را بنویسید...'
            }),
        }
        labels = {
            'text': 'متن نظر',
        }