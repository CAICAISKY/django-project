from django.db.models import F
from django.shortcuts import render, get_object_or_404, get_list_or_404

# Create your views here.
from system.models import News
from utils import constants


def news_info(request, pk):
    """ 新闻详情 """
    news_obj = get_object_or_404(News, pk=pk, is_valid=True)
    news_obj.view_count = F('view_count') + 1
    news_obj.save()
    # 由于此时对象中的view_count变成了`F('view_count') + 1`，所以从新从数据库中获取一次
    news_obj.refresh_from_db()
    return render(request, 'news_info.html', {
        'news_obj': news_obj
    })


def news_list(request):
    """ 新闻列表 """
    # 获取新闻列表: 有效的、新闻类型
    news = get_list_or_404(News, is_valid=True, types=constants.NEWS_TYPE_NEW)
    return render(request, 'news_list.html', {
        'news_list': news
    })
