#!/usr/bin/env python 
# coding: utf-8 -*-
#引入表单类
from django import  forms
#引入模型
from .models import ArticlePost

#添加文章的表单类
class ArticlePostForm(forms.ModelForm):
    class Meta:
        #指出数据模型来源
        model = ArticlePost
        #定义表单包含字段
        fields = ('title','body')