import json

from django.http import HttpResponse
from django.shortcuts import render


def test_ajax(request):
    name = request.GET.get('name')
    return HttpResponse(json.dumps({'result': 'ok', 'name': 'schuyler'}), status=200)


def ajax_html(request):
    return render(request, 'test_form.html')
