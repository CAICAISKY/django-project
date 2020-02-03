from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from accounts.forms import UserLoginForm


def user_login(request):
    """ 用户登陆视图 """
    form = UserLoginForm(request)
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            # 验证通过
            data = form.cleaned_data
            """ 自定的user登录 """
            # user = User.objects.get(username=data['username'], password=data['password'])
            # request.session[constants.LOGIN_USER_ID] = user.id
            """ 使用django的auth模块进行用户登录 """
            user = authenticate(username=data['username'], password=data['password'])
            login(request, user)
            return redirect('index')
        else:
            print(form.errors)
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    """ 用户退出 """
    logout(request)
    return  redirect('index')
