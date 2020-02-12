# Create your views here.
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
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


def product_detail(request, uid):
    """ 商品详情 """
    product = get_object_or_404(Product, uid=uid, is_valid=True)
    address = request.user.default_address
    return render(request, 'product_detail.html', {'product': product, 'address': address})


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
        # 以商品名进行搜索
        name = self.request.GET.get('name', None)
        if name:
            query = query & Q(name__icontains=name)
        # 以标签进行搜索
        tag = self.request.GET.get('tag', '')
        if tag:
            query = query & Q(tags__code=tag)
        # 以分类进行搜索
        cls = self.request.GET.get('cls', '')
        if cls:
            query = query & Q(classes__code=cls)
        product_list = Product.objects.filter(query)
        return product_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_data'] = self.request.GET.dict()
        return context


