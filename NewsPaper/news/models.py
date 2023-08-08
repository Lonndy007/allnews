from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=64) # полное имя автора
    name = models.CharField(null=True, max_length=64)
    rating = models.IntegerField(default=0) #рейтинг

    def update_rating(self):
        post_rating = Post.objects.filter(author=self).aggregate(pr=Coalesce(Sum('rating'),0))['pr']
        comments_rating = Comment.objects.filter(user=self).aggregate(cr=Coalesce(Sum('rating'),0))['cr']
        posts_comments_rating = Comment.objects.filter(post__author=self).aggregate(pcr=Coalesce(Sum('rating'),0))['pcr']

        print(post_rating)
        print('-----')
        print(comments_rating)
        print('-----')
        print(posts_comments_rating)

        self.rating = post_rating * 3 + comments_rating + posts_comments_rating
        self.save()
class Category(models.Model):
    name_of_category = models.CharField(max_length=100,unique=True)#название категории и ее уникальность

class Post(models.Model):
    author = models.ForeignKey(Author,on_delete=models.CASCADE) #связь один ко многим с автором
    news = 'NW'
    article = 'AT'
    POSITIONS = [(news,'Новость'),(article,'Статья')]
    position = models.CharField(max_length=2,choices=POSITIONS,default=news)
    time_of_add = models.DateTimeField(auto_now_add=True) #время добавления
    post_category = models.ManyToManyField(Category, through='PostCategory')#связь с доп моделью посткатегори и категори
    header = models.CharField(max_length=100,unique=True)#заголовок статьи
    text_of_news = models.TextField()#текст
    rate_of_news = models.IntegerField(default=0) #рейтинг статьи


    def like_post(self):
        self.rate_of_news += 1
        self.save()


    def dislike_post(self):
        self.rate_of_news -= 1
        self.save()

    def preview(self):
        return self.text_of_news[0:124]



class PostCategory(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)#связь многи ко многим с пост
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)#связь с пост
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text_of_comm = models.CharField(max_length=800)#текст комментария
    time_of_comm = models.DateTimeField(auto_now_add=True)#время добавления
    rate_of_comm = models.IntegerField(default=0)#рейтинг


    def like(self):
        self.rate_of_comm += 1
        self.save()

    def dislike(self):
        self.rate_of_comm -= 1
        self.save()















