import uuid as uuid

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from accounts.models import User
from system.models import ImageFile
from utils import constants


class BaseModel(models.Model):
    """ 基础模型 """
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        abstract = True


class Classify(BaseModel):
    """ 商品的分类 """
    uid = models.UUIDField('分类ID', default=uuid.uuid4(), editable=False)
    parent = models.ForeignKey('self', related_name='children', verbose_name='商品分类自关联', on_delete=True)
    code = models.CharField('编码', max_length=32, null=True, blank=True)
    img = models.ImageField('分类主图', upload_to='classify')
    name = models.CharField('名称', max_length=12)
    desc = models.CharField('描述', max_length=64, null=True, blank=True)
    reorder = models.SmallIntegerField('排序', default=0)
    is_valid = models.BooleanField('是否有效', default=True)

    class Meta:
        db_table = 'mall_classify'
        ordering = ['-reorder']


class Tag(BaseModel):
    """ 商品的标签 """
    uid = models.UUIDField('分类ID', default=uuid.uuid4(), editable=False)
    img = models.ImageField('分类主图', upload_to='classify')
    code = models.CharField('编码', max_length=32, null=True, blank=True)
    name = models.CharField('名称', max_length=12)
    reorder = models.SmallIntegerField('排序', default=0)
    is_valid = models.BooleanField('是否有效', default=True)

    class Meta:
        db_table = 'mall_tag'


class Product(BaseModel):
    """ 商品模块 """
    uid = models.UUIDField('商品id', default=uuid.uuid4(), editable=False)
    name = models.CharField('商品名称', max_length=128)
    desc = models.CharField('简单描述', max_length=256, null=True, blank=True)
    content = models.TextField('商品描述')
    types = models.SmallIntegerField(
        '商品类型',
        choices=constants.PRODUCT_TYPES_CHOICES,
        default=constants.PRODUCT_TYPE_ACTUAL
    )
    price = models.IntegerField('兑换价格(积分兑换)')
    origin_price = models.FloatField('原价')
    img = models.ImageField('主图', upload_to='product')
    buy_link = models.CharField('购买连接', max_length=256, null=True, blank=True)
    reorder = models.SmallIntegerField('排序', default=0)
    status = models.SmallIntegerField(
        '商品状态',
        choices=constants.PRODUCT_STATUS_CHOICES,
        default=constants.PRODUCT_STATUS_OFF
    )
    is_valid = models.BooleanField('是否有效', default=True)

    tags = models.ManyToManyField(Tag, verbose_name='标签', related_name='tags', blank=True)
    classes = models.ManyToManyField(Classify, verbose_name='分类', related_name='classes', blank=True)
    banners = GenericRelation(ImageFile, verbose_name='banner图', related_query_name='banners')

    class Meta:
        db_table = 'mall_product'
        ordering = ['-reorder']


class Comments(BaseModel):
    """ 商品评价 """
    product = models.ForeignKey(Product, on_delete=True, related_name='comments', verbose_name='商品')
    user = models.ForeignKey(User, related_name='comments', verbose_name='用户', on_delete=True)
    reorder = models.SmallIntegerField('排序', default=0)
    is_anonymous = models.BooleanField('是否匿名', default=0)

    score = models.FloatField('商品评分', default=10.0)
    score_deliver = models.FloatField('配送服务分', default=10.0)
    score_package = models.FloatField('快递包装分', default=10.0)
    score_speed = models.FloatField('送货速度分', default=10.0)

    is_valid = models.BooleanField('是否有效', default=True)
    img_list = GenericRelation(ImageFile,
                               verbose_name='评价晒图',
                               related_query_name='img_list')

    class Meta:
        db_table = 'mall_comments'
        ordering = ['-reorder']
