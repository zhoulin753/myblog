$(function () {

    if (window.location.pathname==='/enter/' || window.location.pathname==='/enroll/'){
        $('body').css({background:'url("../../static/img/timg背景.jpg")',width:'100%' , height:'100%'})
    }
    else {
        $('body').css({background:'#dee7de',width:'100%' , height:'100%'})
    }
    var ret_blog = /^\/blog\/[a-zA-Z0-9]+/,
        ret_write = /^\/write/;
    var path = window.location.pathname,
        ret_article = /^\/[a-zA-Z0-9]+\/article\/\d+/;

    if(ret_blog.test(path) || ret_article.test(path) || ret_write.test(path)){
        $('.div23').animate({
            height:'250px'
        },2000);
        $('.div22').animate({
            top:'220px'
        },2000)
    }
    var $enter_enroll = $('.enter_enroll'),
        $div16 = $('.div16'),
        $button2 = $('.button2'),
        $text1 = $('.text1'),
        $div26 = $('.div26');
    //实现验证码的换图
    $('.span1').click(function () {
        $(this).siblings().attr('src', $(this).siblings().attr('src') + '?')
    });

    //实现注册数据后台验证
    $('.input5').click(function () {
        var $formdate = new FormData();
        $('.input1').each(function () {
            $formdate.append($(this).attr('name'), $(this).val())
        });
        var file = $('.input2')[0].files[0];
        $formdate.append('file', file);
        console.log($formdate);
        console.log($.cookie('csrftoken'));
        $.ajax({
            url: '/enroll_validate/',
            type: 'POST',
            data: $formdate,
            processData: false,
            contentType: false,
            headers: {"x-CSRFToken": $.cookie('csrftoken')},
            success: function (date) {
                if (date['state'] === '200') {
                    window.location.href = '/enter/'
                }
                else {
                    $('.input1').each(function () {
                        $(this).next().html('');
                        $(this).next().html(date[$(this).attr('name')]).css({
                            color: 'red',
                            position: 'relative',
                            float: 'right',
                            fontSize: 1
                        }).siblings().css(
                            {borderColor: 'red'}
                        );
                        if ($(this).next().html() === '') {
                            $(this).css({borderColor: '#ccc'})
                        }
                    })
                }

            }
        })
    });

    //实现图片浏览
    $('.input2').change(function () {
        var file = $(this)[0].files[0];
        var reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function () {
            $('.img2').attr('src', this.result)
        }
    });

    //将登录页面的数据传到
    $('.button1').click(function () {
        var a = 0, $input3 = $('.input3');
        $input3.each(function () {
            a += 1;
            $(this).css({borderColor: ''}).next().html('');
            if ($(this).val() === '') {
                $(this).css({borderColor: 'red'}).next().html('不可为空！').css({color: 'red', fontSize: 1, float: 'right'})
            }
        });
        if (a === 3 && $('.input4').val() !== '') {
            var $formdata = new FormData();
            $formdata.append('user', $('.input6').val());
            $formdata.append('password', $('.input7').val());
            $formdata.append('vail', $('.input8').val());
            // console.log($.cookie('csrftoken'));
            $.ajax({
                url: '/enter/',
                type: 'POST',
                data: $formdata,
                contentType: false,
                processData: false,
                headers: {'x-CSRFToken': $.cookie('csrftoken')},
                success: function (data) {
                    console.log(data);
                    if (data['sate'] === '200') {
                        // alert(document.referrer);
                        if (document.referrer === 'http://127.0.0.1:8000/enroll/'){
                            window.location.href = 'http://127.0.0.1:8000'
                        }
                        else {
                            // alert(document.referrer);
                            window.location.href = document.referrer
                        }
                    }
                    else {
                        $input3.each(function () {
                            $(this).next().html('');
                            $(this).next().html(data[$(this).attr('name')]);
                        })
                    }
                }
            })
        }
    });

    if ($enter_enroll.html() === 'True') {

        $button2.click(function () {
            $div26.css({display: 'none'});
            if ($text1.val() === '') {
                $div26.css({display: 'block'})
            }
            else {

                var $formdata = new FormData();
                $formdata.append('comment', $text1.val());
                $formdata.append('article_id', $div16.siblings('a').attr('href').split('/')[2]);
                $formdata.append('username',$enter_enroll.attr('title'));
                $formdata.append('parent_id','');
               console.log($formdata);
                $.ajax({
                    url: '/comment/',
                    type: 'post',
                    data: $formdata,
                    contentType: false,
                    processData: false,
                    headers: {'x-CSRFToken': $.cookie('csrftoken')},
                    success: function (data) {

                        var $li = $('<li class="list-group-item"><span > '
                            +data['username']+' </span><span>'+data['time']+
                            '</span><a href="#textarea" class="pull-right">评论()' +
                            '</a> <span class="pull-right">点赞()</span><span class="pull-right">' +
                            '踩()</span><hr class="hr1"><span>'+data['comment']+'</span>');
                        $('.ul19').append($li);
                        $('.text1').val('')
                    }

                })
            }
        });
    }
    else {

        $button2.on('click', function () {
            // $(this).attr('aria-describedby','popover770584');
            $(this).attr('data-target', '#myModal');
        })
    }



    // if ($enter_enroll.html()) {
    //
    //     var send_ajax = function ($element, what, zh, str, user, article) {
    //         var $formdata = new FormData();
    //         $formdata.append('what', what);
    //         $formdata.append('username', user);
    //         $formdata.append('article_id', article);
    //         $.ajax({
    //             url: '/up_down/',
    //             type: 'post',
    //             data: $formdata,
    //             processData: false,
    //             contentType: false,
    //             headers: {'x-CSRFToken': $.cookie('csrftoken')},
    //             success: function (data) {
    //                 var b = str.match(/\(([^)]*)/i);
    //                 var c = parseInt(b[1]) + 1;
    //                 if (data['what'] === 'first') {
    //                     str = zh + '(' + c + ')';
    //                     $element.html(str).css({color: 'blue'})
    //                 }
    //                 else if (data['what'] === 'two') {
    //                     c -= 2;
    //                     str = zh + '(' + c + ')';
    //                     $element.html(str).css({color: ''})
    //                 }
    //                 else if (data['what'] === 'third') {
    //                     if (what === 'up') {
    //                         var str1 = zh + '(' + c + ')',
    //                             str_down = $element.next().html();
    //                         var f = str_down.match(/\(([^)]*)/i)[1],
    //                             g = parseInt(f) - 1;
    //                         str_new_down = '踩' + '(' + g + ')';
    //                         $element.html(str1).css({color: 'blue'}).next().css({color: ''}).html(str_new_down)
    //                     }
    //                     else if (what === 'down') {
    //                         var str1 = zh + '(' + c + ')',
    //                             str_down = $element.prev().html();
    //                         var f = str_down.match(/\(([^)]*)/i)[1],
    //                             g = parseInt(f) - 1;
    //                         str_new_down = '赞' + '(' + g + ')';
    //                         $element.html(str1).css({color: 'blue'}).prev().css({color: ''}).html(str_new_down)
    //                     }
    //                 }
    //             }
    //         })
    //     };
    //
    //     $div16.on('click', '.vote', function () {
    //         var $element = $(this),
    //             str = $(this).html(),
    //             ret = /^赞\(\d+\)$/,
    //             ret_down = /^踩\(\d+\)$/,
    //             user = '{{ request.user.username }}',
    //             article = $(this).parent().siblings('a').attr('href').split('/')[2];
    //         if (ret.test(str)) {
    //             send_ajax($element, 'up', '赞', str, user, article)
    //         }
    //         else if (ret_down.test(str)) {
    //             send_ajax($element, 'down', '踩', str, user, article)
    //         }
    //     });
    // }
    // else {
    //     $div16.on('click', '.vote', function () {
    //         $(this).attr('data-target', '#myModal');
    //     })
    // }
    $('.wangEditor-menu-container').change(function () {
        $(this).css({position:'static',top:'auto',width:'100%'})
    });
    $('#drop4').click(function () {
        $(this).addClass('open').children('a:eq(0)').attr('aria-expanded','true').next('ul').css({display:'block'});

    });
    var send_category = function (languange,author) {
        var $formdata = new FormData();
        $formdata.append('language',languange);
        $formdata.append('author',author);
        $.ajax({
            url:'/category',
            type:'post',
            data:$formdata,
            processData: false,
            contentType: false,
            headers: {"x-CSRFToken": $.cookie('csrftoken')},
            success:function (data) {
                if (data['author']==='') {

                    $('.div10').html(data['html'])
                }
                else {

                    $('.div15').html(data['html'])
                }
            }
        })
    };
    $('.classa').click(function () {
        if ($(this).attr('name')===undefined){
            //那就是主页的分类
            send_category($(this).attr('title'),'')
        }
        else{
            //blog个人的分类
            send_category($(this).attr('name'),$(this).attr('title'));
        }
    })





});