from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models import F

from utils import constants


class BaseModel(models.Model):
    """ 基础模型类 """
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    """ 用户基础信息 """
    # username = models.CharField('用户名', max_length=64)
    # password = models.CharField('密码', max_length=256)
    avatar = models.ImageField('用户头像', upload_to='avatar', null=True, blank=True)
    integral = models.IntegerField('用户积分', default=0)
    nickname = models.CharField('昵称', max_length=32)
    level = models.SmallIntegerField('用户级别', default=1)
    is_valid = models.BooleanField('是否有效', default=1)

    class Meta:
        db_table = 'accounts_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    @property
    def default_address(self):
        """ 获取默认地址，如果没有设置，则获取第一个 """
        default_address = None
        address_list = self.user_address.filter(is_valid=True)
        try:
            default_address = address_list.filter(is_default=True)[0]
        except IndexError:
            try:
                default_address = address_list[0]
            except IndexError:
                pass
        return default_address

    def integral_oper(self, num, type=1):
        """
        修改点券
        :param type: 操作类型， 0为扣分、1为充值
        :param num: 操作的点数
        """
        if type == 0:
            self.integral = F('integral') - abs(num)
        else:
            self.integral = F('interral') + abs(num)
        self.save()


class UserProfile(BaseModel):
    """ 用户详细信息 """
    user = models.OneToOneField(User, on_delete=True, verbose_name='关联用户')
    real_name = models.CharField('真实姓名', max_length=32)
    sex = models.SmallIntegerField('性别', choices=constants.USER_SEX_CHOICES, default=constants.USER_SEX_MAN)
    age = models.SmallIntegerField('年龄', default=0)
    email = models.CharField('电子邮箱', null=True, blank=True, max_length=128)
    phone_no = models.CharField('手机号码', null=True, blank=True, max_length=20)
    is_email_valid = models.BooleanField('邮箱是否验证', default=False)
    is_phone_valid = models.BooleanField('手机是否验证', default=False)

    class Meta:
        db_table = 'accounts_user_profile'


class UserAddress(BaseModel):
    """ 用户地址 """
    user = models.ForeignKey(User, on_delete=True, verbose_name='关联用户', related_name='user_address')
    province = models.CharField('省份', max_length=32)
    city = models.CharField('城市', max_length=32)
    area = models.CharField('区域', max_length=32)
    town = models.CharField('街道', max_length=32, null=True, blank=True)
    address = models.CharField('详细地址', max_length=64)
    username = models.CharField('收件人', max_length=32)
    phone = models.CharField('收件人电话', max_length=32)

    is_default = models.BooleanField('是否为默认地址', default=False)
    is_valid = models.BooleanField('是否有效', default=True)

    class Meta:
        db_table = 'accounts_user_address'
        ordering = ['is_default', '-updated_at']
        verbose_name = '用户地址'
        verbose_name_plural = '用户地址'

    def get_phone_format(self):
        """ 获取屏蔽后的手机号码 """
        return self.phone[0: 3] + "****" + self.phone[7:]

    def get_region(self):
        """ 获取省市区的合拼地址 """
        region = '{self.province} {self.city} {self.area}'.format(self=self)
        return region


class LoginRecord(models.Model):
    """ 登陆历史 """
    user = models.ForeignKey(User, on_delete=True, verbose_name='关联用户', related_name='user_login_record')
    username = models.CharField('登陆的账号', max_length=64)
    ip = models.CharField('IP', max_length=32)
    address = models.CharField('地址', max_length=32, null=True, blank=True)
    source = models.CharField('登陆的来源', max_length=32)

    created_at = models.DateTimeField('登陆时间', auto_now_add=True)

    class Meta:
        db_table = 'accounts_login_record'


class PasswordChangeLog(models.Model):
    """ 密码修改记录 """
    user = models.ForeignKey(User, on_delete=True, verbose_name='关联用户', related_name='user_password_log')
    ip = models.CharField('IP', max_length=32)
    address = models.CharField('地址', max_length=32, null=True, blank=True)
    source = models.CharField('登陆的来源', max_length=32)
    oldpwd = models.CharField('旧密码', max_length=256)
    newpwd = models.CharField('新密码', max_length=256)

    created_at = models.DateTimeField('密码修改时间', auto_now_add=True)

    class Meta:
        db_table = 'accounts_password_change_log'
