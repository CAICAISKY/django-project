from django.http import HttpResponse, FileResponse
from django.views.generic import TemplateView


def test_one(request):
    file = open('medias/timg.jpeg', 'rb')
    return FileResponse(file, content_type='image/jpeg')


def test_two(request):
    return HttpResponse("test_two")


def page_404(request, exception):
    return HttpResponse("404异常")


class ShowClassView(TemplateView):
    template_name = "test_class_view.html"
