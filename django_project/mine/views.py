# Create your views here.
from django.views.generic import DetailView

from mine.models import Order


class OderDetailView(DetailView):
    """ 订单详情视图 """
    model = Order
    template_name = 'order_info.html'
    slug_url_kwarg = 'sn'
    slug_field = 'sn'
    context_object_name = 'order'
