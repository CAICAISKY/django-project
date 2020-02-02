from django import forms

from django_study.models import WeiboImg, Content


# class UserForm(forms.ModelForm):
#     """ 模型表单 """
#     class Meta:
#         model = User
#         fields = ['username', 'password', 'nickname']
#         widgets = {
#             'password': forms.PasswordInput(
#                 attrs={
#                     'class': 'pwd'
#                 }
#             )
#         }
#         labels = {
#             'username': '手机号',
#             'password': '密码'
#         }
#         error_messages = {
#             'username': {
#                 'required': '请输入手机号码'
#             }
#         }
#         help_texts = '帮助文字'


class WeiboImgForm(forms.ModelForm):
    """ 微博图片模型表单 """
    content = forms.CharField(label='评论内容', widget=forms.Textarea)

    class Meta:
        model = WeiboImg
        fields = ['image']

    def save(self, commit=True):
        """ 重写父类save函数，来修改外键数据 """
        # 获取当前模型表单的模型对象
        obj = super().save(commit=False)
        content = self.cleaned_data['content']
        content_obj = Content.objects.create(content=content)
        obj.content = content_obj
        obj.save()
        return obj

