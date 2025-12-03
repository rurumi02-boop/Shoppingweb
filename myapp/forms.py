from django import forms
from .models import User
from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='密碼'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='確認密碼'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        labels = {
            'username': '帳號',
            'email': '電子郵件',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password and confirm and password != confirm:
            raise ValidationError("密碼與確認密碼不一致")
        return cleaned_data