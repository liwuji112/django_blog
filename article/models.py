from django.db import models

# Create your models here.
#导入内建的User模型
from django.contrib.auth.models import User
#timezone用于处理时间相关事务
from django.utils import timezone


#博客文章数据模型
class ArticlePost(models.Model):
    #文章作者 on_delete 用于指定数据删除的方式 作者在用户当中挑选 作者属于用户 外键写在被属于那方
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='作者')
    title = models.CharField(max_length=100, verbose_name='文章标题')
    # 文章正文。保存大量文本使用 TextField
    body = models.TextField()

    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    total_views = models.PositiveIntegerField(default=0)

    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-created', )

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        return self.title
