from django import template

# 获取注册对象
register = template.Library()


def my_filter(value):
    """ 使首字母变红 """
    if value:
        value = "<span style='color:red;'>" + value[0] + "</span>" + value[1:]
    return value


# 注册过滤器
register.filter('my_filter', my_filter)