# Create your views here.
from django.shortcuts import render_to_response, render


def product_list(request, template_name='product_list.html'):
    return render_to_response(template_name)


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
    return render(request, 'test.html', data)
