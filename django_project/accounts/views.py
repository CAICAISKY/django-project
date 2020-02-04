from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from accounts.forms import UserLoginForm, UserRegisterForm, UserAddressForm
from accounts.models import User, UserAddress
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


@login_required
def password_change(request):
    """ 密码修改 """
    result = ''
    if request.method == 'POST':
        vc = VerifyCode(request)
        vcode = request.POST.get('vcode')
        if vc.validate_code(vcode):
            user = request.user
            new_password = request.POST.get('password')
            user.set_password(new_password)
            return redirect('index')
        else:
                result = '验证码错误！'
    return render(request, 'pwd_change.html', {
        'result': result
    })


@login_required
def address_list(request):
    """ 地址列表 """
    user_address_list = UserAddress.objects.filter(is_valid=True, user=request.user)

    return render(request, 'address_list.html', {
        'user_address_list': user_address_list
    })


@login_required
def address_edit(request, pk):
    """ 地址修改/新增 """
    user_address = None
    initial = {}
    if pk.isdigit():
        """ 当传入了主键后 """
        user_address = get_object_or_404(UserAddress, pk=pk, user=request.user, is_valid=True)
        initial['region'] = user_address.get_region()
    if request.method == 'POST':
        form = UserAddressForm(request=request, data=request.POST, instance=user_address, initial=initial)
        if form.is_valid():
            form.save()
            return redirect('accounts:address_list')
    else:
        form = UserAddressForm(request=request, instance=user_address, initial=initial)
    return render(request, 'address_edit.html', {
        'form': form
    })


@login_required
def address_delete(request, pk):
    """ 删除地址 """
    address = get_object_or_404(UserAddress, pk=pk, is_valid=True, user=request.user)
    address.is_valid = False
    address.save()
    return HttpResponse('ok')
