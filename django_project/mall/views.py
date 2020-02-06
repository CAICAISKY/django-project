# Create your views here.
from django.db.models import Q
from django.shortcuts import render_to_response, render
from django.views.generic import ListView

from mall.models import Product
from utils import constants


def product_list(request):
    """ 商品列表 """
    product_list = Product.objects.filter(status=constants.PRODUCT_STATUS_SELL, is_valid=True)
    name = request.GET.get('name', None)
    if name:
        product_list = Product.objects.filter(status=constants.PRODUCT_STATUS_SELL, is_valid=True, name__icontains=name)
        print(product_list.count())
    return render(request, 'product_list.html', {
        'product_list': product_list
    })


def product_detail(request, pk, template_name='product_detail.html'):
    return render_to_response(template_name)


def filter_test(request):
    data = {
        'data_list': [
            '第一行',
            '第二行',
            '第三行'
        ]
    }
    return render(request, 'test_form.html', data)


class ProduceListView(ListView):
    # 配置渲染的模版文件
    template_name = 'product_list.html'
    # 每一页的个数
    paginate_by = 6
    # 设置结果集变量名称
    context_object_name = 'product_list'

    def get_queryset(self):
        """ 获取结果集的函数 """
        query = Q(status=constants.PRODUCT_STATUS_SELL, is_valid=True)
        name = self.request.GET.get('name', None)
        if name:
            query = query & Q(name__icontains=name)
        product_list = Product.objects.filter(query)
        print(product_list)
        return product_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_data'] = self.request.GET.dict()
        return context


