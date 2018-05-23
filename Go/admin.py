from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register([User,Article,ArticleDescribe,Website,ArticleDescribe2Label,ArticleUpDown,CommentUp,Comment,Category,Label,])

