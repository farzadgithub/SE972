from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class SignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'نام کاربری'}),
                               label='نام کاربری',
                               required=True,
                               disabled=False,
                               help_text='')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'نام'}),
                                 label='نام',
                                 required=True,
                                 disabled=False,
                                 help_text='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'نام خانوادگی'}),
                                label='نام خانوادگی',
                                required=True,
                                disabled=False,
                                help_text='')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور'}),
                                label='رمز عبور',
                                required=True,
                                disabled=False,
                                help_text='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'تکرار رمز عبور'}),
                                label='تکرار رمز عبور',
                                required=True,
                                disabled=False,
                                help_text='')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'ایمیل'}),
                             label='ایمیل',
                             max_length=64,
                             help_text='یک ایمیل معتبر وارد کنید')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')