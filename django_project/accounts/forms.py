import re

from django import forms
from django.contrib.auth import authenticate

from accounts.models import User, UserAddress
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


class UserAddressForm(forms.ModelForm):
    """ 用户地址模型表单 """
    region = forms.CharField(label='省市区', max_length=64, error_messages={
        'required': '请填写省市区'
    })

    class Meta:
        model = UserAddress
        fields = ['username', 'phone', 'address', 'is_default']
        widgets = {
            'is_default': forms.CheckboxInput(
                attrs={
                    'class': 'weui-switch'
                }
            )
        }
        error_messages = {
            'username': {
                'required': '请填写收件人！'
            },
            'phone': {
                'required': '请填写手机号码！'
            },
            'address': {
                'required': '请填写详细地址！'
            }
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_phone(self):
        """ 验证手机号码 """
        pattern = r'^1{1}[0-9]{10}$'
        phone = self.cleaned_data['phone']
        result = re.search(pattern, phone)
        if not result:
            raise forms.ValidationError('请填写正确的手机号码！')
        return phone

    def save(self, commit=True):
        """ 整理模型数据 """
        address_obj = super().save(False)
        (province, city, area) = self.cleaned_data['region'].split(' ')
        address_obj.province = province
        address_obj.city = city
        address_obj.area = area
        address_obj.user = self.request.user

        # 设定为默认地址时，先去除其他默认地址
        if self.cleaned_data['is_default']:
            UserAddress.objects.filter(user=self.request.user, is_valid=True, is_default=True).update(is_default=False)

        address_obj.save()
        return address_obj
