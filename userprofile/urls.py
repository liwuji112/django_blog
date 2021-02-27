#!/usr/bin/env python 
# -*-coding: utf-8 -*-
# 开发团队: 奶豆的小铺
# 开发人员: bcz
# 开发时间: 2021/2/24 21:48
#正在部署的app名称

from django.urls import path
from . import views


app_name = 'userprofile'
urlpatterns = [
    path('login/', views.user_login, name='user_login'),  #登录页
    path('register/', views.user_register, name='user_register'),  #注册页
    path('logout/', views.user_logout, name='user_logout'),  #登录退出页
    # 用户删除
    path('delete/<int:id>/', views.user_delete, name='user_delete'),
    # 用户信息
    path('edit/<int:id>/', views.profile_edit, name='user_edit'),
]
