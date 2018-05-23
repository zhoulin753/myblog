from django.forms import Form, widgets, fields
from .models import *
from django.http import JsonResponse


class MyForm(Form):
    name1 = fields.CharField(max_length=16, min_length=5, required=True,
                             error_messages={
                                 'required': '用户名不可以为空',
                                 'min_length': '长度不可小于5',
                                 'max_length': '长度不可大于16'
                             },
                             widget=widgets.TextInput(attrs={
                                 'class': 'form-control input1',
                                 'id': 'inputEmil1',
                                 'placeholder': '昵称：',
                                 'name': 'name1'
                             }))
    name2 = fields.CharField(max_length=10, min_length=5,
                             error_messages={
                                 'required': '用户名不可以为空',
                                 'min_length': '请输入合法的姓名',
                                 'max_length': '请输入合法的姓名'
                             },
                             widget=widgets.TextInput(attrs={
                                 'class': 'form-control input1',
                                 'id': 'inputEmil2',
                                 'placeholder': '请输入你的姓名：',
                                 'required': '用户名不可以为空',
                                 'name': 'name2'
                             }))
    phone = fields.CharField(max_length=11, min_length=11,
                             error_messages={
                                 # 'required': '用户名不可以为空',
                                 'min_length': '请输入合法的电话',
                                 'required': '用户名不可以为空',
                                 'max_length': '请输入合法的电话'
                             },
                             widget=widgets.TextInput(attrs={
                                 'class': 'form-control input1',
                                 'id': 'inputEmil3',
                                 'placeholder': '请输入你的电话：',
                                 'name': 'phone'
                             }))
    email = fields.EmailField(label='请输入你的邮箱：',
                              error_messages={'invalid': '格式错误'},
                              widget=widgets.EmailInput(attrs={
                                  'name': 'email',
                                  'class': 'form-control input1',
                                  'id': 'inputEmail6',

                                  'placeholder': '请输入Email:'

                              }))
    password = fields.CharField(max_length=20, min_length=8,
                                error_messages={
                                    'max_length': '最大长度超过20',
                                    'min_length': '长度没有超过8'
                                },
                                widget=widgets.PasswordInput(attrs={
                                    'name': 'password',
                                    'class': 'form-control input1',
                                    'id': 'inputEmail4',
                                    'placeholder': '请输入密码：'
                                }))
    password_code = fields.CharField(max_length=20, min_length=8,
                                     error_messages={
                                         'max_length': '最大长度超过20',
                                         'min_length': '长度没有超过8'
                                     },
                                     widget=widgets.PasswordInput(attrs={
                                         'name': 'password_code',
                                         'class': 'form-control input1',
                                         'id': 'inputEmail5',
                                         'placeholder': '请再次输入密码'
                                     }))
    verification = fields.CharField(max_length=6, min_length=6,
                                    error_messages={
                                        'max_length': '你输入的验证码错误',
                                        'min_length': '你输入的验证码错误'
                                    },
                                    widget=widgets.TextInput(attrs={
                                        'name': 'verification',
                                        'class': 'form-control input1',
                                        'id': 'inpurtPassword',
                                        'placeholder': '请输入验证码：'
                                    }))
