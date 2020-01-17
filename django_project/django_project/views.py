from datetime import datetime

from django.shortcuts import render

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
    print(news_list)
    return render(request, "index.html", {
        'slider_list': slider_list,
        'news_list': news_list
    })
