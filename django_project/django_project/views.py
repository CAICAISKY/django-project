from datetime import datetime

from django.shortcuts import render

from mall.models import Product
from system.models import Slider, News
from utils import constants


def index(request):
    slider_list = Slider.objects.filter(types=constants.SLIDER_TYPE_INDEX)
    time_now = datetime.now()
    news_list = News.objects.filter(
        types=constants.NEWS_TYPE_NEW,
        is_top=True,
        is_valid=True,
        start_time__lte=time_now,
        end_time__gte=time_now
    )
    # 获取精选推荐商品列表
    jxtj_list = Product.objects.filter(is_valid=True, status=constants.PRODUCT_STATUS_SELL, tags__code='jxtj')
    # 获取酒水推荐商品列表
    jstj_list = Product.objects.filter(is_valid=True, status=constants.PRODUCT_STATUS_SELL, tags__code='jstj')
    # 获取猜你喜欢商品列表
    cnxh_list = Product.objects.filter(is_valid=True, status=constants.PRODUCT_STATUS_SELL, tags__code='cnxh')
    return render(request, "index.html", {
        'slider_list': slider_list,
        'news_list': news_list,
        'jxtj_list': jxtj_list,
        'jstj_list': jstj_list,
        'cnxh_list': cnxh_list
    })
