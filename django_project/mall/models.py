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
    uid = models.UUIDField('分类ID', default=uuid.uuid4, editable=False)
    parent = models.ForeignKey('self',
                               related_name='children',
                               verbose_name='商品分类自关联',
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    code = models.CharField('编码', max_length=32, null=True, blank=True)
    img = models.ImageField('分类主图', upload_to='classify')
    name = models.CharField('名称', max_length=12)
    desc = models.CharField('描述', max_length=64, null=True, blank=True)
    reorder = models.SmallIntegerField('排序', default=0)
    is_valid = models.BooleanField('是否有效', default=True)

    class Meta:
        db_table = 'mall_classify'
        ordering = ['-reorder']
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'

    def __str__(self):
        return '{}:{}'.format(self.code, self.name)


class Tag(BaseModel):
    """ 商品的标签 """
    uid = models.UUIDField('标签ID', default=uuid.uuid4(), editable=False)
    img = models.ImageField('标签主图', upload_to='classify')
    code = models.CharField('编码', max_length=32, null=True, blank=True)
    name = models.CharField('名称', max_length=12)
    reorder = models.SmallIntegerField('排序', default=0)
    is_valid = models.BooleanField('是否有效', default=True)

    class Meta:
        db_table = 'mall_tag'
        verbose_name = '商品标签'
        verbose_name_plural = '商品标签'

    def __str__(self):
        return '{}:{}'.format(self.code, self.name)


class Product(BaseModel):
    """ 商品模块 """
    # 商品模块的主键id不应该暴露出来，容易被别人爬取商品数据，因此设置一个uid字段来作为索引
    uid = models.UUIDField('商品id', default=uuid.uuid4(), editable=False)
    name = models.CharField('商品名称', max_length=128)
    desc = models.CharField('简单描述', max_length=256, null=True, blank=True)
    content = models.TextField('商品描述', null=True, blank=True)
    types = models.SmallIntegerField(
        '商品类型',
        choices=constants.PRODUCT_TYPES_CHOICES,
        default=constants.PRODUCT_TYPE_ACTUAL
    )
    price = models.IntegerField('兑换价格(积分兑换)')
    origin_price = models.FloatField('原价')
    img = models.ImageField('主图', upload_to='%Y%m/product')
    buy_link = models.CharField('购买连接', max_length=256, null=True, blank=True)
    reorder = models.SmallIntegerField('排序', default=0)
    status = models.SmallIntegerField(
        '商品状态',
        choices=constants.PRODUCT_STATUS_CHOICES,
        default=constants.PRODUCT_STATUS_OFF
    )

    sku_count = models.IntegerField('库存', default=0)
    ramain_count = models.IntegerField('剩余库存', default=0)
    view_count = models.IntegerField('浏览次数', default=0)
    score = models.FloatField('商品的评分', default=10.0)

    is_valid = models.BooleanField('是否有效', default=True)

    tags = models.ManyToManyField(Tag, verbose_name='标签', related_name='tags', blank=True)
    classes = models.ManyToManyField(Classify, verbose_name='分类', related_name='classes', blank=True)
    banners = GenericRelation(ImageFile, verbose_name='banner图', related_query_name='banners')

    class Meta:
        db_table = 'mall_product'
        ordering = ['-reorder']
        verbose_name = '商品信息'
        verbose_name_plural = '商品信息'

