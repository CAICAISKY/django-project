from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from utils import constants


class BaseModel(models.Model):
    """ 基础模型 """
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('最后修改时间', auto_now=True)

    class Meta:
        abstract = True


class Slider(BaseModel):
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

    class Meta:
        db_table = 'system_slider'
        ordering = ['-reorder']
        verbose_name = '轮播图'
        verbose_name_plural = '轮播图'


class News(BaseModel):
    """ 新闻及通知 """
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

    class Meta:
        db_table = 'system_news'
        ordering = ['-reorder']
        verbose_name = '新闻/通知'
        verbose_name_plural = '新闻/通知'


class ImageFile(BaseModel):
    """ 图片表 用于存放其他模块图片数据"""
    # 因为有文件数量限制，因此定义文件夹为YYYYmm/xxxx
    img = models.ImageField('图片', upload_to='%Y%m/images/')
    summary = models.CharField('图片名称', max_length=200)

    # 复合关联
    content_type = models.ForeignKey(ContentType, on_delete=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    is_valid = models.BooleanField('是否有效', default=True)

    class Meta:
        db_table = 'system_images'
        verbose_name = '图片库'
        verbose_name_plural = '图片库'
