from django.db import models

# Create your models here.


class Content(models.Model):
    """ 评论用户 """
    content = models.TextField('评论内容')
    created_at = models.DateTimeField('评论时间', auto_now_add=True)


class WeiboImg(models.Model):
    """ 微博图片 """
    image = models.ImageField('微博图片', upload_to='weibo')
    content = models.ForeignKey(Content, on_delete=True)
