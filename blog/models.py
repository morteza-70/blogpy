from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.timezone import now
from DateTime import DateTime


def validate_file_extension(values):
    import os
    from django.core.exceptions import ValidationError

    ext = os.path.splitext(values.name)[1]
    valid_extensions = ['.jpg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extention')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FileField(upload_to='files/user_avatar/', null=False, blank=False)
    description = models.CharField(max_length=512, null=False, blank=False)

class Article(models.Model):
    title = models.CharField(max_length=128, null=False, blank=False)
    cover = models.FileField(upload_to='files/article/cover', null=False, blank=False)
    content = RichTextField()
    created_at = models.DateTimeField(default=now, null=False, blank=False)
    category = models.ForeignKey('category', on_delete=models.CASCADE)
    author = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

class Category(models.Model):
    title = models.CharField(max_length=128, null=False, blank=False)
    cover = models.FileField(upload_to='files/category_cover', null=False, blank=False)

    def __str__(self):
        return self.title