from django import forms
from django.contrib.auth import authenticate

from accounts.models import User
from utils.verify_code import VerifyCode


class UserLoginForm(forms.Form):
    """ 用户登陆表单 """
    vcode = forms.CharField(label='验证码', max_length=4, error_messages={'required': '请填入验证码！'})
    username = forms.CharField(label='用户名', max_length=150, error_messages={'required': '请输入用户名！'})
    password = forms.CharField(label='密码', max_length=128, error_messages={'required': '请输入密码！'})

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    # def clean_username(self):
    #     """ 校验用户名 """
    #     pattern = r'1{0,1}[0-9]{10}'
    #     username = self.cleaned_data['username']
    #     result = re.search(pattern, username)
    #     if not result:
    #         raise forms.ValidationError('请输入正确手机号码！')
    #     return username

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
            if not authenticate(username=username, password=password):
                raise forms.ValidationError('密码错误')
        return cleaned_data


class UserRegisterForm(forms.ModelForm):
    """ 用户注册表单，这里使用auth模块的User """
    # 验证码
    vcode = forms.CharField(label='验证码', max_length=4, error_messages={'required': '请输入验证码！'})
    # 重复密码
    repassword = forms.CharField(
        label='重复密码',
        max_length=128,
        error_messages={'required': '请重复密码！'},
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'nickname']
        error_messages = {
            'username': {
                'required': '请输入用户名！',
                'unique': '用户名已存在！'
            },
            'nickname': {
                'required': '请输入昵称！'
            },
            'password': {
                'required': '请输入密码！'
            }
        }
        widgets = {
            'password': forms.PasswordInput
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_repassword(self):
        """ 重复密码的校验 """
        data = self.cleaned_data
        password = data['password']
        repassword = data['repassword']
        if password != repassword:
            raise forms.ValidationError('密码不一致！')
        return repassword

    def clean_vcode(self):
        """ 验证码校验 """
        vcode = self.cleaned_data['vcode']
        vc = VerifyCode(self.request)
        if not vc.validate_code(code=vcode):
            raise forms.ValidationError('验证码不正确！')
        return vcode
