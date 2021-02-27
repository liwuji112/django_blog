from django.urls import path
from article import views

#正在部署的app名称
app_name = 'article'
urlpatterns = [
    path('list/', views.article_list, name='article_list'),  #首页
    path('detail/<int:id>/',views.article_detail,name='article_detail'),#详情页面
    path('create/',views.article_create,name='article_create'),#添加文章页面
    path('delete/<int:id>/',views.article_delete,name='article_delete'),#添加文章页面
    path('update/<int:id>/',views.article_update,name='article_update'),#添加文章页面
]
