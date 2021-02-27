#!/usr/bin/env python 
# -*-coding: utf-8 -*-
# 开发团队: 奶豆的小铺
# 开发人员: bcz
# 开发时间: 2021/2/24 21:48

from  django import  forms
from django.contrib.auth.models import  User
from .models import Profile

'''
而`forms.Form`则需要手动配置每个字段，**它适用于不与数据库进行直接交互的功能**。
用户登录不需要对数据库进行任何改动，因此直接继承`forms.Form`就可以了。'''
#登录表单
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


# Profile的表单类
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # 定义表单包含的字段
        fields = ('phone', 'avatar', 'bio')

#用户注册表单
class UserRegisterForm(forms.ModelForm):
    # 复写 User 的密码
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        #因为password字段上边已经改写，所以不需要写入这个字段
        fields=('username','email')


    #类的实例方法
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise  forms.ValidationError('两次密码输入不一致，请从新输入')