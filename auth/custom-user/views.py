from django.shortcuts import render,redirect
from .forms import registerationForm
from django.contrib import messages
from django.conf import settings
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from .utils import send_activation_email
from .models import User
from django.contrib.auth import authenticate,login

def login_view(request):
    if request.user.is_authenticated:
       if request.user.is_recruiter:
           return redirect('rDashboard')
       elif request.user.is_applicant:
           return redirect('dashboard')
       return redirect('home')
    
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        if not email or not password:
            messages.error(request,"Both fields are required")
            return redirect('login')
        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request,"Invalid Email or password")
            return redirect('login')
        
        if not user.is_active:
            messages.error(request,'Your account is inactive please activate it ')
            return redirect('login')
        user=authenticate(request,email=email,password=password)

        if user is not None:
            login(request,user)
            if request.user.is_recruiter:
              return redirect('rDashboard')
            elif request.user.is_applicant:
              return redirect('dashboard')
        else:
            messages.error(request,'Invalid email or password')
    return render(request,'account/login.html')


def register_view(request):
    if request.method=="POST":
        form=registerationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active=False
            user.save()
            uidb64=urlsafe_base64_encode(force_bytes(user.pk))
            token=default_token_generator.make_token(user)
            activation_link=reverse('activate',kwargs={'uidb64':uidb64,'token':token})
            activation_url=f'{settings.SITE_DOMAIN}{activation_link}'
            send_activation_email(user.email,activation_url)
            messages.success(request,'Registeration Successfull please check your email for to activate account')
            return redirect('login')
        else:
            # This will show errors in template
            return render(request, 'account/register.html', {'form': form})
    else:
        form=registerationForm()

    return render(request,'account/register.html',{'form':form})