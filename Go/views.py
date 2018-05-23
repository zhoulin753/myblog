from django.shortcuts import render, HttpResponse, redirect
#laijiang2
# from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .models import *


def index(request):
    uname = '首页'
    artivle_list = ArticleDescribe.objects.filter()
    category_list = Category.objects.filter()
    return render(request, 'Go/index.html', locals())


def enter(request):
    uname = '登录'
    if request.is_ajax():
        user = request.POST.get('user')
        password1 = request.POST.get('password')
        vail = request.POST.get('vail').lower()
        if vail == ("").join(request.session.get('verification').lower().split(' ')):
            if User.objects.filter(username=user) or User.objects.filter(email=user) or User.objects.filter(phone=user):
                m = User.objects.filter(username=user)
                n = User.objects.filter(email=user)
                b = User.objects.filter(phone=user)
                c = [m, n, b]
                for i in c:
                    if not i:
                        continue
                    else:
                        # 登录不上的原因不是数据的问题，而是authenticate会加密，而password1是明文所以
                        # 匹配出错
                        user = authenticate(username=user, password=password1)
                        if user:
                            login(request, user)
                            return JsonResponse({'sate': '200', })
                        else:
                            return JsonResponse({'password': '密码输入错误！'})
            else:
                return JsonResponse({'user': '不存在的用户！'})
        else:
            return JsonResponse({'vail': '验证码输入错误！'})

    return render(request, 'Go/enter.html', locals())


def enroll(request):
    uname = '注册'
    myform = MyForm()
    return render(request, 'Go/enroll.html', locals())


def img(request):
    from PIL import Image, ImageDraw, ImageFont
    from io import BytesIO
    import random
    import string
    a = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),)
    image = Image.new(mode='RGB', size=(180, 40), color=a)
    draw = ImageDraw.Draw(image, mode='RGB')
    verification = ' '.join(random.sample(string.digits + string.ascii_letters, 6))
    request.session['verification'] = verification
    font_style = ImageFont.truetype('Go/static/fonts/hakuyoxingshu7000.TTF', 28)
    draw.text((20, 10), verification, font=font_style)
    f = BytesIO()
    image.save(f, 'png')
    return HttpResponse(f.getvalue())


def enroll_validate(request):
    if request.is_ajax():
        myform = MyForm(request.POST)
        if myform.is_valid():
            name1 = myform.cleaned_data['name1']
            name2 = myform.cleaned_data['name2']
            password = myform.cleaned_data['password']
            password_code = myform.cleaned_data['password_code']
            phone = myform.cleaned_data['phone']
            email = myform.cleaned_data['email']
            verification = myform.cleaned_data['verification']
            session = ('').join(request.session.get('verification').lower().split(' '))
            verification_lower = verification.lower()
            file = request.FILES
            if verification_lower == session:
                if password == password_code:
                    if not User.objects.filter(username=name1):
                        if not User.objects.filter(phone=phone):
                            if file.get('file'):
                                a = file.get('file')
                            else:
                                a = 'Go/static/img/default.jpg'
                            user = User.objects.create_user(
                                username=name1, first_name='blog', last_name=name2,
                                password=password, phone=phone,
                                email=email, avatar=a
                            )
                            user.save()
                            return JsonResponse({'state': '200', 'url': ''})
                        else:
                            return JsonResponse({'phone': '电话不合法，已经存在'})
                    else:
                        return JsonResponse({'name1': '用户名已存在！'})
                else:
                    return JsonResponse({'password': '两次输入不一样', 'password_code': '两次输入不一样'})
            else:
                return JsonResponse({'verification': '验证码输入错误'})
        else:
            my = myform.errors
            return JsonResponse(my)


def chulishuju(request, user):
    user_list = User.objects.filter(username=user)
    if not user_list:
        return render(request, '404.html')
    use = user_list.first()
    fans = use.userfans.count()
    ariticle = ArticleDescribe.objects.filter(user__username=user)
    category = Category.objects.filter(website__blog__username=user)
    a = []
    for i in category:
        a.append((i, ariticle.filter(corresponding__language=i).count()))
    return a, use, ariticle, category, fans


def blog(request, user):
    uname = user
    use = user_list = User.objects.get(username=user)

    a, use, ariticle_list, category, fans = chulishuju(request, user)

    return render(request, 'Go/blog.html', locals())


def article_num(request, user_name, num):
    article_describe = ArticleDescribe.objects.get(id=num)
    use = article_describe.user
    a, use, ariticle, category, fans = chulishuju(request, use)
    uname = use.username
    comment_count = article_describe.comment_set.count()
    ariticle_comment = Comment.objects.filter(article=ariticle)
    return render(request, 'Go/article.html', locals())


def log_out(request):
    logout(request)
    return redirect('/')


def up_down(request):
    information = request.POST
    print(information)
    username = information['username']
    article_id = information['article_id']
    str = information['str']
    user_id = User.objects.get(username=username).pk
    a = ArticleUpDown.objects.filter(user__id=user_id).values_list()
    if information['what'] == 'up':
        if a:
            for i in a:
                if i[1] == user_id and i[2] == int(article_id):
                    if i[3]:
                        ArticleUpDown.objects.filter(user__id=user_id).get(article__id=article_id).delete()
                        article = ArticleDescribe.objects.get(id=article_id)
                        article.up_count = ArticleUpDown.objects.filter(is_up=True, article=article).count()
                        article.down_count = ArticleUpDown.objects.filter(is_up=False, article=article).count()
                        article.save()
                        return JsonResponse({'what': 'two', 'str': str})
                    else:
                        down = ArticleUpDown.objects.filter(user_id=user_id).get(article_id=article_id)
                        article = ArticleDescribe.objects.get(id=article_id)
                        article.up_count = ArticleUpDown.objects.filter(is_up=True, article=article).count()
                        article.down_count = ArticleUpDown.objects.filter(is_up=False, article=article).count()
                        article.save()
                        down.is_up = 1
                        down.save()
                        return JsonResponse({'what': 'third', 'str': str})
        up = ArticleUpDown.objects.create(is_up=1, user_id=user_id, article_id=article_id)
        article = ArticleDescribe.objects.get(id=article_id)
        article.up_count = ArticleUpDown.objects.filter(is_up=True, article=article).count()
        article.down_count = ArticleUpDown.objects.filter(is_up=False, article=article).count()
        article.save()
        up.save()
        return JsonResponse({'what': 'first', 'str': str})
    else:
        if a:
            for i in a:
                if i[1] == user_id and i[2] == int(article_id):
                    if not i[3]:
                        ArticleUpDown.objects.filter(user_id=user_id).get(article_id=article_id).delete()
                        article = ArticleDescribe.objects.get(id=article_id)
                        article.up_count = ArticleUpDown.objects.filter(is_up=True, article=article).count()
                        article.down_count = ArticleUpDown.objects.filter(is_up=False, article=article).count()
                        article.save()
                        return JsonResponse({'what': 'two', 'str': str})
                    else:
                        down = ArticleUpDown.objects.filter(user_id=user_id).get(article_id=article_id)
                        down.is_up = 0
                        article = ArticleDescribe.objects.get(id=article_id)
                        article.up_count = ArticleUpDown.objects.filter(is_up=True, article=article).count()
                        article.down_count = ArticleUpDown.objects.filter(is_up=False, article=article).count()
                        article.save()
                        down.save()
                        return JsonResponse({'what': 'third', 'str': str})
        up = ArticleUpDown.objects.create(is_up=0, user_id=user_id, article_id=article_id)
        article = ArticleDescribe.objects.get(id=article_id)
        article.up_count = ArticleUpDown.objects.filter(is_up=True, article=article).count()
        article.down_count = ArticleUpDown.objects.filter(is_up=False, article=article).count()
        article.save()
        up.save()
        return JsonResponse({'what': 'first', 'str': str})


def comment(request):
    comment1 = request.POST.get('comment')
    username = request.POST.get('username')
    user = User.objects.get(username=username)
    article_id = request.POST.get('article_id')
    article = ArticleDescribe.objects.get(id=article_id)
    comment_count = article.comment_count
    comment_count += 1
    article.comment_count = comment_count
    article.save()
    comment = Comment.objects.create(content=comment1, user=user, article=article, )
    return JsonResponse({'time': str(comment.create_time)[:19], 'user': username, 'comment': comment1})


def write(request):
    uname = 'write'
    a, use, ariticle, category, fans = chulishuju(request, request.user.username)

    return render(request, 'Go/write.html', locals())


def category(request):
    if request.is_ajax():
        author = request.POST.get('author')
        language = request.POST.get('language')
        print(author)
        if author:
            print(type(author))
            print( ArticleDescribe.objects.filter(user__username=author))
            html = ''
            article_list = ArticleDescribe.objects.filter(user__username=author, corresponding__language=language)
            print(222)
            for i in article_list:

                model = '<li><div class ="media" ><div class ="media-body h4_color">' \
                        '<h4 class ="media-heading h5_color" ><a href="/' + i.user.username + '/article/' + str(
                    i.pk) + '"'  + ' class ="a2" > ' + i.title + '</a></h4 ><a href = "/' + i.user.username + '/article/' + str(i.pk) + '" ' \
                            'class ="a1" >' + i.article_describe + '</a><div class ="div16" >' \
                                                                   '<span style = "display: none"> <a href = "blog/' + i.user.username + '">' + i.user.username + ' </a> </span>' \
                                                                                                                                                                        '<span> 发布于：' + str(i.create_time) + ' </span ><span> 阅读数： </span>' \
                                                                                                                                                                                                          '<span> 评论数：' + str(i.comment_count) + ' </span ><span class ="glyphicon glyphicon-thumbs-up up_span vote" data-toggle="modal">' \
                                                                                                                                                                                                                                              ' 赞(' + str(i.up_count) + ') </span><span class ="glyphicon glyphicon-thumbs-down down_span vote" data-toggle="modal">' \
                                                                                                                                                                                                                                                   ' 踩(' + str(i.down_count) + ')</span></div></div></div><hr></li>'
                html += model
            html=html+'<nav aria-label="..."><ul class="pager"><li class="previous li1"><a href="#" class="a9"><span aria-hidden="true">&larr;</span> 上一页</a></li>' \
                            '<li class="next li1"><a href="#" class="a9">下一页 <span aria-hidden="true">&rarr;</span></a></li>' \
                            '</ul></nav>'
            return JsonResponse({'html': html, 'author': author})
        else:
            #主页的编辑
            html = ''
            article_list = ArticleDescribe.objects.filter(corresponding__language=language)
            for i in article_list:
                model = '<li><div class="media"><div class="media-left"><a class="a3" href="blog/'+i.user.username+'">' \
                        '<img class="media-object img_avatar" data-src="holder.js/64x64" alt="64x64" src="'+str(i.user.avatar)+'" ' \
                        'data-holder-rendered="true"></a></div><div class="media-body h4_color">' \
                        '<h4 class="media-heading h5_color"><a href="'+i.user.username+'/article/'+str(i.pk)+'" ' \
                        'class="a2">'+i.title+'</a></h4><a href="'+i.user.username+'/article/'+str(i.pk)+'" ' \
                        'class="a1">'+i.article_describe+'</a><div class="div16"><span><a href="/blog/'+i.user.username+'">'+i.user.username+'</a></span>' \
                        '<span>发布于：'+str(i.create_time)+'</span><span>阅读数：66</span><span>评论数：'+str(i.comment_count)+'</span>' \
                        '<span class="glyphicon glyphicon-thumbs-up up_span vote" data-toggle="modal">' \
                        '赞('+str(i.up_count)+')</span><span class="glyphicon glyphicon-thumbs-down down_span vote" data-toggle="modal">' \
                        '踩('+ str(i.down_count)+')</span></div></div></div><hr></li>'
                html += model
            html = html+'<nav aria-label="..."><ul class="pager"><li class="previous li1"><a href="#" class="a9"><span aria-hidden="true">&larr;</span> 上一页</a></li>' \
                            '<li class="next li1"><a href="#" class="a9">下一页 <span aria-hidden="true">&rarr;</span></a></li>' \
                            '</ul></nav>'
            return JsonResponse({'html': html, 'author': ''})
