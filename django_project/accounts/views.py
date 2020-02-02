from django.shortcuts import render, redirect

from accounts.forms import UserLoginForm
from accounts.models import User
from utils import constants


def user_login(request):
    """ 用户登陆视图 """
    form = UserLoginForm(request)
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            # 验证通过
            data = form.cleaned_data
            user = User.objects.get(username=data['username'], password=data['password'])
            request.session[constants.LOGIN_USER_ID] = user.id
            return redirect('index')
        else:
            print(form.errors)
    return render(request, 'login.html', {'form': form})

