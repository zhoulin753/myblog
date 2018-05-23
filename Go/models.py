from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    avatar = models.FileField(upload_to='media/upload/avatar', default='static/img/default.jpg')
    phone = models.CharField(max_length=11, null=True, unique=True)
    # userfans=models.ManyToManyField(through='UserFans',to='self',
    #                                 verbose_name='粉丝',
    #                                 through_fields=('user','follower')
    #                                 )
    userfans = models.ManyToManyField('self')

    def __str__(self):
        return self.username


# class UserFans(models.Model):
#     user = models.ForeignKey(to='User',verbose_name='博主')
#     follower = models.ForeignKey(to = 'User' , verbose_name='粉丝')
#
#     class Meta:
#         unique_together=[
#             ('user','follower')
#         ]


class Website(models.Model):
    # url=models.CharField(max_length=20)
    # user=models.ForeignKey('User')
    title = models.CharField(max_length=64)
    site = models.CharField(max_length=32)
    theme = models.CharField(max_length=23)
    blog = models.OneToOneField('User')

    def __str__(self):
        return self.title


class Category(models.Model):
    language = models.CharField(max_length=20)
    # article=models.ForeignKey('ArticleDescribe')
    website = models.ForeignKey('Website')

    def __str__(self):
        return self.language


class Label(models.Model):
    # 标签
    name = models.CharField(max_length=20)
    website = models.ForeignKey('Website', )

    def __str__(self):
        return self.name


class ArticleDescribe(models.Model):
    # 文章描述
    title = models.CharField(max_length=40)
    article_describe = models.CharField(max_length=255)
    create_time = models.DateField()
    comment_count = models.IntegerField()
    up_count = models.IntegerField()
    down_count = models.IntegerField()
    user = models.ForeignKey('User')
    # website=models.ForeignKey(Website)
    corresponding = models.ForeignKey('Category')
    lable = models.ManyToManyField(to='Label', through='ArticleDescribe2Label', through_fields=('article', 'label'), )

    def __str__(self):
        return self.title


class Article(models.Model):
    # 文章详细表
    article = models.TextField()
    articleDescribe = models.OneToOneField('ArticleDescribe')

    def __str__(self):
        return self.articleDescribe.title


class Comment(models.Model):
    # 平论
    create_time = models.DateTimeField(auto_now_add=True)
    parent_id = models.ForeignKey('self', default=None, null=True)
    article = models.ForeignKey('ArticleDescribe')
    user = models.ForeignKey('User')
    content = models.CharField(max_length=225)

    def __str__(self):
        return self.user


class CommentUp(models.Model):
    # 品论点赞表
    user = models.ForeignKey('User', null=True)
    is_up = models.ForeignKey('Comment', null=True)


class ArticleUpDown(models.Model):
    user = models.ForeignKey('User')
    article = models.ForeignKey('ArticleDescribe')
    is_up = models.BooleanField(default=True)

    class Meta:
        unique_together = [
            ('article', 'user')
        ]


class ArticleDescribe2Label(models.Model):
    article = models.ForeignKey('ArticleDescribe')
    label = models.ForeignKey('Label')

    class Meta:
        unique_together = [
            ('article', 'label')
        ]
