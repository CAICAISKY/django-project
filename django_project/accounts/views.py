from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from accounts.forms import UserLoginForm, UserRegisterForm
from accounts.models import User
from utils.verify_code import VerifyCode


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


def user_register(request):
    """ 用户注册 """
    form = UserRegisterForm(request)
    if request.method == 'POST':
        form = UserRegisterForm(request, data=request.POST)
        if form.is_valid():
            # 注册验证通过，将用户注册到数据库中
            data = form.cleaned_data
            User.objects.create_user(username=data['username'], password=data['password'])
            # 登录
            user = authenticate(username=data['username'], password=data['password'])
            login(request, user)
            return redirect('index')
        else:
            print(form.errors)
    return render(request, 'regist.html', {
            'form': form
        })


def password_change(request):
    """ 密码修改 """
    result = ''
    if request.method == 'POST':
        vc = VerifyCode(request)
        vcode = request.POST.get('vcode')
        user = request.user
        if user.is_authenticated:
            if vc.validate_code(vcode):
                new_password = request.POST.get('password')
                user.set_password(new_password)
                return redirect('index')
            else:
                result = '验证码错误！'
        else:
            result = '用户未登录'
    return render(request, 'pwd_change.html', {
        'result': result
    })
