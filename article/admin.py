from django.contrib import admin

# Register your models here.
from article.models import ArticlePost


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'updated')
    '''
    这是在view中模糊查询的字段，其中submitter字段是一个外键ForeignKey字段，而作为一个外键，它所对应的不是一个具体的字段，而是一个类。
    所以我们应该将其对应成为一个外键关联的摸一个具体的字段，如submitter__username
    '''
    search_fields = ('title', 'author__username', 'body')


admin.site.register(ArticlePost, ArticleAdmin)
