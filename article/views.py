from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from article import views
from article.forms import ArticlePostForm
from article.models import ArticlePost
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

import markdown
# Create your views here.

# def article_list(request):
#     return HttpResponse("hello djagno!")


'''
6、Paginator介绍
使用Paginator分页，更多请参考官方文档：https://docs.djangoproject.com/en/2.1/topics/pagination/
必须的参数：
object_list：可为列表、元组、Queryset或可迭代的
per_page：每一页的数据的数量
属性:
（1）、count
（2）、num_pages:返回总页数
（3）、page_range:返回一个所有页面迭代器
方法：
（1）、page(num):返回所指定的页面对象，不存在的会引发错误
Page对象的方法：
（1）、page.has_next()：判断当前页是否有下一页
（2）、page.has_previous()：判断当前页是否有上一页
'''
#文章列表
def article_list(request):
    #取出所有文章
    articles = ArticlePost.objects.all()
    currentPage = int(request.GET.get('page', 1))  # 获取当前在第几页
    # 实例化文章分页对象
    paginator = Paginator(articles, 5)  # 告诉分页器我5条分页
    # 如果总页数大于十一页，设置分页
    if paginator.num_pages > 11:
        # 如果当前页数小于5页
        if currentPage - 5 < 1:
            # 页面上显示的页码
            pageRange = range(1, 11)
        #     如果当前页数+5大于总页数显示的页码
        elif currentPage + 5 > paginator.num_pages:
            pageRange = range(paginator.num_pages - 9, paginator.num_pages + 1)
        else:
            # 在中间显示的十个页码
            pageRange = range(currentPage - 5, currentPage + 5)
    else:
        pageRange = paginator.page_range
    #     捕获路由异常
    try:
        article_obj = paginator.page(currentPage)
    #     如果页码输入不是整数则返回第一页的数据
    except PageNotAnInteger:
        article_obj = paginator.page(1)
    #     如果页码输入是空值则返回第一页数据
    except EmptyPage:
        article_obj = paginator.page(1)
    # article_obj.has_previous = article_obj.has_previous()
    # article_obj.has_next = article_obj.has_next()
    #需要传给模板的对象
    context = {
        'articles': article_obj,
        'pageRange':pageRange,
        'currentPage':currentPage,
    }
    print(article_obj.has_previous())
    # render函数：载入模板，并返回context对象
    return render(request, 'article_list.html', context=context)


'''
这里有一个bug
打开django/views下的debug.py文件，331行：
把
with Path(CURRENT_DIR, 'templates', 'technical_500.html').open() as fh
改成：
with Path(CURRENT_DIR, 'templates', 'technical_500.html').open(encoding="utf-8") as fh
应该就可以了
'''
#文章详情页面
@login_required(login_url='/user/login/')
def article_detail(request,id=1):
    #获取指定id的文章
    article= ArticlePost.objects.get(id = id)#不知 原因是什么 必须用id
    article.total_views +=1
    # `update_fields = []
    # `指定了数据库只更新`
    # total_views
    # `字段，优化执行效率。
    article.save(update_fields=['total_views'])
    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         # 包含 缩写、表格等常用扩展
                                         'markdown.extensions.extra',
                                         # 语法高亮扩展
                                         'markdown.extensions.codehilite',
                                     ])
    #放入上下文context
    context = {
        'article':article,
    }
    return render(request,'article_detail.html',context=context)


#写文章的视图函数
@login_required(login_url='/user/login/')
def article_create(request):
    if request.method =='POST':
        #将request.post提交上来的数据添加到表单当中

        article_post_form = ArticlePostForm(data = request.POST)
        #判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            new_article =ArticlePost()
            #保存数据，但是先不提交到数据库
            # new_article = article_post_form.save(commit=False)
            new_article.title = request.POST['title']
            new_article.body = request.POST['body']
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            print(request.user.id)
            new_article.author = User.objects.get(id = request.user.id)
            # 将新文章保存到数据库中
            new_article.save()
            return redirect('article:article_list')
        else:
            return HttpResponse('表单提交有误，请重新添写')
    # 如果用户请求获取数据
    else:
        #markdown渲染没有实现
        # 修改 Markdown 语法渲染
        md = markdown.Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        #创建表单实例
        article_post_form = ArticlePostForm()
        #赋值上下文
        context = {
            'article_post_form':article_post_form,
        }
        #返回模板
        return render(request,'article_create.html',context=context)



#删除文章的视图
@login_required(login_url='/user/login/')
def article_delete(request,id=1):
    #获取到要删除的文章
    article = ArticlePost.objects.get(id = id)
    #调用delete方法删除
    if request.user == article.author:
        article.delete()
    #完成删除后返回文章列表
    else:
        return HttpResponse('您无权删除该文章')

    return redirect('article:article_list')




#修改文章的视图函数
@login_required(login_url='/user/login/')
def article_update(request,id=1):
    #获取文章
    article = ArticlePost.objects.get(id = id)
    if request.user !=article.author:
        return HttpResponse('您无权对此文章进行修改！')
    if request.method =='POST':
        #将request.post提交上来的数据添加到表单当中
        article_post_form = ArticlePostForm(data = request.POST)
        #判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            #保存数据，但是先不提交到数据库
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect('article:article_detail',id = id)
        else:
            return HttpResponse('表单提交有误，请重新添写')
    # 如果用户请求获取数据
    else:
        #markdown渲染没有实现
        # # 修改 Markdown 语法渲染
        # md = markdown.Markdown(
        #     extensions=[
        #         'markdown.extensions.extra',
        #         'markdown.extensions.codehilite',
        #         'markdown.extensions.toc',
        #     ]
        # )
        #创建表单实例
        article_post_form = ArticlePostForm()

        #赋值上下文
        context = {
            'article':article,
            'article_post_form':article_post_form,
        }
        #返回模板
        return render(request,'article_update.html',context=context)


