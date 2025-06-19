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

def activate_account(request, uidb64, token):
    try:
        # 🔓 Decode the base64-encoded user ID from the URL
        uid = force_str(urlsafe_base64_decode(uidb64))
        
        # 🔍 Try to fetch the user with the decoded ID
        user = User.objects.get(pk=uid)

        # ⚠️ If user is already active, no need to activate again
        if user.is_active:
            messages.warning(request, "This account has already been activated")
            return redirect('login')

        # ✅ Check if the token is valid for this user
        if default_token_generator.check_token(user, token):
            # 🟢 Activate the user account
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated successfully')
            return redirect('login')
        else:
            # ❌ Token is invalid or expired
            messages.error(request, "The activation link is invalid or expired")
            return redirect('login')

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        # ❗ Any error in decoding or user lookup
        messages.error(request, "Invalid activation link")
        return redirect('login')
