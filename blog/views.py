from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers

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

class ContactPage(TemplateView):
    template_name = 'page-contact.html'

class AboutPage(TemplateView):
    template_name = 'page-about.html'

class CategoryPage(TemplateView):
    template_name = 'category.html'

class ArticleAPIView(TemplateView):

    def get(self, request, format=None):
        try:
            all_articles = Article.objects.all().order_by('-created_at')[:5]
            data = []

            for article in all_articles:
                data.append({
                    "title": article.title,
                    "cover": article.cover.url if article.cover else None,
                    "content": article.content,
                    "created_at": article.created_at,
                    "category": article.category.title,
                    "author": article.author,
                    "promote": article.promote,
                })

            return Response({'data': data}, status=status.HTTP_200_OK)
        
        except:
            return Response({'status': "Internal Server Error, We'll Check It Later" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class SingleArticleAPIView(APIView):
    
    def get(self, request, format=None):
        try:
            article_title = request.GET['article_title']
            article = Article.objects.filter(title__contains=article_title)
            serialized_data = serializers.SingleArticleSerializers(article, many=True)
            data = serialized_data.data

            return Response({'data': data}, status=status.HTTP_200_OK)

        except:
            return Response({'status': "Internal Server Error, We'll Check It Later" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# search in articles with api
class SearchArticleAPIView(APIView):
    
    def get(self, request, format=None):
        try:
            from django.db.models import Q

            query = request.GET['query']
            articles = Article.objects.filter(Q(content__icontains=query))
            data = []

            for article in articles:
                data.append({
                    "title": article.title,
                    "cover": article.cover.url if article.cover else None,
                    "content": article.content,
                    "created_at": article.created_at,
                    "category": article.category.title,
                    "author": article.author.user.first_name + ' ' + article.author.user.last_name,
                    "promote": article.promote,
                })

            return Response({'data': data}, status=status.HTTP_200_OK)

        except:
            return Response({'status': "Internal Server Error, We'll Check It Later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# submit articles with api
class SubmitArticleAPIView(APIView):

    def post(self, request, format=None):

        try:
            serializer = serializers.SubmitArticleSerializer(data=request.data)
            if serializer.is_valid():
                title = serializer.data.get('title')
                cover = request.FILES['cover']
                content = serializer.data.get('content')
                category_id = serializer.data.get('category_id')
                author_id = serializer.data.get('author_id')
                promote = serializer.data.get('promote')
            else:
                return Response({'status':'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(id=author_id)
            author = UserProfile.objects.get(user=user)
            category = Category.objects.get(id=category_id)

            article = Article()
            article.title = title
            article.cover = cover
            article.content = content
            article.category = category
            article.author = author
            article.promote = promote
            article.save()

            return Response({'status': 'OK'}, status=status.HTTP_200_OK)

        except:
            return Response({'status': "Internal Server Error, We'll Check It Later"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
