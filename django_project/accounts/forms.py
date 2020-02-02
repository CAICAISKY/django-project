import re

from django import forms

from accounts.models import User
from utils.verify_code import VerifyCode


class UserLoginForm(forms.ModelForm):
    """ 用户登陆表单 """
    vcode = forms.CharField(label='验证码', max_length=4, error_messages={'required': '请填入验证码！'})

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_username(self):
        """ 校验用户名 """
        pattern = r'1{0,1}[0-9]{10}'
        username = self.cleaned_data['username']
        result = re.search(pattern, username)
        if not result:
            raise forms.ValidationError('请输入正确手机号码！')
        return username

    def clean_vcode(self):
        vcode = self.cleaned_data['vcode']
        vc = VerifyCode(self.request)
        result = vc.validate_code(vcode)
        if not result:
            raise forms.ValidationError('验证码错误！')
        return vcode

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username', None)
        password = cleaned_data.get('password', None)
        if username and password:
            user_list = User.objects.filter(username=username)
            if not user_list.exists():
                raise forms.ValidationError('用户名不存在')
            if not user_list.filter(password=password).exists():
                raise forms.ValidationError('密码错误')
        return cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']
        error_messages = {
            'username': {
                'required': '请输入用户名！'
            },
            'password': {
                'required': '请输入密码！'
            }
        }
