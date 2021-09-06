from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *

# Create your views here.
class IndexPage(TemplateView):
    
    def get(self, request, **kwargs):
        article_data = []
        all_articles = Article.objects.order_by('-created_at').all()[:9]

        for article in all_articles:
            article_data.append({
                'title': article.title,
                'cover': article.cover.url,
                'category': article.category.title,
                'created_at': article.created_at.date(),
            })
        
        promote_data = []
        all_promote_articles = Article.objects.filter(promote=True)
        for promote_articles in all_promote_articles:
            promote_data.append({
                'category': promote_articles.category.title,
                'title': promote_articles.title,
                'cover': promote_articles.cover.url if promote_articles.author.avatar else None,
                'author': promote_articles.author.user.first_name + ' ' + promote_articles.author.user.last_name,
                'avatar': promote_articles.author.avatar.url if promote_articles.author.avatar else None,
                'created_at': promote_articles.created_at.date(),
            })

        context = {
            'article_data': article_data,
            'promote_articles_data': promote_data,
        }

        return render(request,'index.html', context)