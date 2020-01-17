from django.db import models

from utils import constants


class Slider(models.Model):
    """ 轮播图模型 """
    name = models.CharField('名称', max_length=32)
    desc = models.CharField('描述', max_length=100, null=True, blank=True)
    types = models.SmallIntegerField(
        '展现位置',
        choices=constants.SLIDER_TYPES_CHOICES,
        default=constants.SLIDER_TYPE_INDEX
    )
    img = models.ImageField('图片', upload_to='slider')
    reorder = models.SmallIntegerField('排序', default=0, help_text='数字越大，越靠前')
    target_url = models.CharField('跳转地址', null=True, blank=True, max_length=255)

    is_valid = models.BooleanField('是否生效', default=True)
    start_time = models.DateTimeField('生效开始时间', null=True, blank=True)
    end_time = models.DateTimeField('生效结束时间', null=True, blank=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('最后修改时间', auto_now=True)

    class Meta:
        db_table = 'system_slider'
        ordering = ['-reorder']


class News(models.Model):
    """ 新闻即通知 """
    types = models.SmallIntegerField(
        '类型',
        choices=constants.NEWS_TYPES_CHOICES,
        default=constants.NEWS_TYPE_NEW
    )
    title = models.CharField('标题', max_length=255)
    content = models.TextField('内容')
    reorder = models.SmallIntegerField('排序', default=0, help_text='数字越大，越靠前')
    is_top = models.BooleanField('是否置顶', default=True)
    view_count = models.IntegerField('浏览次数', default=0)

    is_valid = models.BooleanField('是否生效', default=True)
    start_time = models.DateTimeField('生效开始时间', null=True, blank=True)
    end_time = models.DateTimeField('生效结束时间', null=True, blank=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('最糊修改时间', auto_now=True)

    class Meta:
        db_table = 'system_news'
        ordering = ['-reorder']
