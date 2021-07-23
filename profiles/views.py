from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.views.generic import UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import get_user_model

from .forms import SignUpForm
from .models import Profile
from .utils import get_location_from_ip
from .tokens import account_activation_token

User = get_user_model()

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        location = request.POST['location']
    else:

        return render(request, 'index.html', {})


def account_activation_sent_view(request):
    return render(request, 'registration/account_activation_sent.html')


def account_activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        print(uid)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        print(e)
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('users:dashboard')
    else:
        return render(request, 'registration/account_activation_invalid.html')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "app/profile_edit.html"
    fields = ('bio',)
