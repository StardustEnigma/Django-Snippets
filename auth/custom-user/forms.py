from django import forms
from .models import User

class registerationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    confirmPassword=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=["email","name","password","confirmPassword"]
    def clean(self):
        cleaned_data=super().clean()
        password=cleaned_data.get('password')
        confirmPassword=cleaned_data.get('confirmPassword')

        if password != confirmPassword:
            self.add_error('confirmPassword','confirm password and password did not match')

        return cleaned_data
    
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists")
        return email 