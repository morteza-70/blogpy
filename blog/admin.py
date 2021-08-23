from django.contrib import admin
from .models import *

# admin.site.register(UserProfile)
# admin.site.register(Category)
# admin.site.register(Article)

class UserProfilAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar', 'description']

admin.site.register(UserProfile, UserProfilAdmin)


class ArticleAdmin(admin.ModelAdmin):
    search_fields = ['title', 'content']
    list_display = ['title', 'category', 'created_at']

admin.site.register(Article, ArticleAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'cover']

admin.site.register(Category, CategoryAdmin)