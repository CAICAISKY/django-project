""" 系统模块-轮播图位置常量 """
SLIDER_TYPE_INDEX = 11
SLIDER_TYPES_CHOICES = (
    (SLIDER_TYPE_INDEX, '首页'),
)

""" 系统模块-新闻常量 """
NEWS_TYPE_NEW = 11
NEWS_TYPE_NOTICE = 12
NEWS_TYPES_CHOICES = (
    (NEWS_TYPE_NEW, '新闻'),
    (NEWS_TYPE_NOTICE, '通知'),
)

""" 用户模块-性别 """
USER_SEX_MAN = 1
USER_SEX_WOMAN = 0
USER_SEX_CHOICES = (
    (USER_SEX_MAN, '男'),
    (USER_SEX_WOMAN, '女')
)

""" 商品模块-商品类别 """
PRODUCT_TYPE_ACTUAL = 11
PRODUCT_TYPE_VIRTUAL = 12
PRODUCT_TYPES_CHOICES = (
    (PRODUCT_TYPE_ACTUAL, '实物商品'),
    (PRODUCT_TYPE_VIRTUAL, '虚拟商品')
)

""" 商品模块-商品状态 """
PRODUCT_STATUS_SELL = 11
PRODUCT_STATUS_LOST = 12
PRODUCT_STATUS_OFF = 13
PRODUCT_STATUS_CHOICES = (
    (PRODUCT_STATUS_SELL, '销售中'),
    (PRODUCT_STATUS_LOST, '已售完'),
    (PRODUCT_STATUS_OFF, '已下架')
)

""" 个人模块-订单状态 """
ORDER_STATUS_INIT = 10
ORDER_STATUS_SUBMIT = 11
ORDER_STATUS_PAID = 12
ORDER_STATUS_SENT = 13
ORDER_STATUS_DONE = 14
ORDER_STATUS_DELETE = 15
ORDER_STATUS_CHOICES = (
    (ORDER_STATUS_SUBMIT, '购物车'),
    (ORDER_STATUS_SUBMIT, '已提交'),
    (ORDER_STATUS_PAID, '已支付'),
    (ORDER_STATUS_SENT, '已发货'),
    (ORDER_STATUS_DONE, '已完成'),
    (ORDER_STATUS_DELETE, '已删除')
)

""" 公用常量 """
LOGIN_USER_ID = 'user_id'
