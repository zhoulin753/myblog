# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
import django.core.validators
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('article', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ArticleDescribe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=40)),
                ('article_describe', models.CharField(max_length=255)),
                ('create_time', models.DateField()),
                ('comment_count', models.IntegerField()),
                ('up_count', models.IntegerField()),
                ('down_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ArticleDescribe2Label',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('article', models.ForeignKey(to='Go.ArticleDescribe')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleUpDown',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('is_up', models.BooleanField(default=True)),
                ('article', models.ForeignKey(to='Go.ArticleDescribe')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('language', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField()),
                ('content', models.CharField(max_length=225)),
                ('article', models.ForeignKey(to='Go.ArticleDescribe')),
                ('parent_id', models.ForeignKey(default=None, to='Go.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='CommentUp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('is_up', models.ForeignKey(null=True, to='Go.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=64)),
                ('site', models.CharField(max_length=32)),
                ('theme', models.CharField(max_length=23)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(verbose_name='username', max_length=30, unique=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], error_messages={'unique': 'A user with that username already exists.'})),
                ('first_name', models.CharField(verbose_name='first name', max_length=30, blank=True)),
                ('last_name', models.CharField(verbose_name='last name', max_length=30, blank=True)),
                ('email', models.EmailField(verbose_name='email address', max_length=254, blank=True)),
                ('is_staff', models.BooleanField(verbose_name='staff status', default=False, help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(verbose_name='active', default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('avatar', models.FileField(default='img/default.jpg', upload_to='Go/static/img/')),
                ('phone', models.CharField(max_length=11, unique=True, null=True)),
                ('groups', models.ManyToManyField(verbose_name='groups', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission')),
                ('userfans', models.ManyToManyField(related_name='userfans_rel_+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='website',
            name='blog',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='label',
            name='website',
            field=models.ForeignKey(to='Go.Website'),
        ),
        migrations.AddField(
            model_name='commentup',
            name='user',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='category',
            name='website',
            field=models.ForeignKey(to='Go.Website'),
        ),
        migrations.AddField(
            model_name='articleupdown',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='articledescribe2label',
            name='label',
            field=models.ForeignKey(to='Go.Label'),
        ),
        migrations.AddField(
            model_name='articledescribe',
            name='corresponding',
            field=models.ForeignKey(to='Go.Category'),
        ),
        migrations.AddField(
            model_name='articledescribe',
            name='lable',
            field=models.ManyToManyField(to='Go.Label', through='Go.ArticleDescribe2Label'),
        ),
        migrations.AddField(
            model_name='articledescribe',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article',
            name='articleDescribe',
            field=models.OneToOneField(to='Go.ArticleDescribe'),
        ),
        migrations.AlterUniqueTogether(
            name='articleupdown',
            unique_together=set([('article', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='articledescribe2label',
            unique_together=set([('article', 'label')]),
        ),
    ]
