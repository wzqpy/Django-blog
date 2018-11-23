
#  forms组件是用于进行  注册条件验证的，可自定义验证规则

from django import forms

from django.forms import widgets

from blog.models import UserInfo

from django.core.exceptions import NON_FIELD_ERRORS, ValidationError


widget1 = widgets.TextInput(attrs={'class':'form-control'})
widget2 = widgets.PasswordInput(attrs={'class':'form-control'})

class UserForm(forms.Form):

    emaill = forms.EmailField(max_length=32,widget=widget1,label='邮箱', error_messages={'required':'该字段不能为空'})
    phone = forms.CharField(max_length=11,widget=widget1,label='电话',error_messages={'required':'该字段不能为空'})
    user = forms.CharField(max_length=32,widget=widget1,label='用户名',error_messages={'required':'该字段不能为空'})
    pwd = forms.CharField(max_length=32,widget=widget2,label='密码',error_messages={'required':'该字段不能为空'})
    re_pwd = forms.CharField(max_length=32,widget=widget2,label='确认密码',error_messages={'required':'该字段不能为空'})

    # 局部钩子
    def clean_user(self):
        '''
        用户验证
        :return:
        '''

        val = self.cleaned_data.get('user')

        user = UserInfo.objects.filter(username=val).first()  #进数据库筛选用户名

        if not user:
            return val
        else:
            raise ValidationError('该用户已注册！')

    def clean_phone(self):

        phone = self.cleaned_data.get('phone')

        if len(phone) == 11:
            return phone
        else:
            raise ValidationError('号码格式有误！')



    # 全局钩子
    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        re_pwd = self.cleaned_data.get('re_pwd')
        if pwd ==re_pwd:
            return self.cleaned_data
        else:
            raise ValidationError('两次密码不一致')