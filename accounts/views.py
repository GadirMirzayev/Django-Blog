from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import  get_user_model
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, DetailView, UpdateView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView



# Create your views here.
from accounts.serializers import UserLoginSerializer
from accounts.forms import RegistrationForm, LoginForm, PasswordChangeForm, EditProfileForm
from accounts.tasks import send_confirmation_mail
from accounts.tools.tokens import account_activation_token

User = get_user_model()


def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # http://example.com
            site_address = request.is_secure() and "https://" or "http://" + request.META['HTTP_HOST']  # https
            send_confirmation_mail(user_id=user.id, site_address=site_address)
            messages.success(request, 'Siz ugurla qeydiyyatdan kecdiniz')
            return redirect(reverse_lazy('stories:home'))
    context = {
        'form': form
    }
    return render(request, 'register.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Email is activated')
        return redirect(reverse_lazy('stories:home'))
    elif user:
        messages.error(request, 'Email is not activated. May be is already activated')
        return redirect(reverse_lazy('accounts:register'))
    else:
        messages.error(request, 'Email is not activated')
        return redirect(reverse_lazy('accounts:register'))


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_serializer = UserLoginSerializer(user)
        if user is not None:
            django_login(request, user)
            messages.success(request, 'Siz ugurla daxil oldunuz.')
        return Response(user_serializer.data, )


class LoginView(TemplateView):
    template_name = 'login.html'


class LogoutView(LoginRequiredMixin ,APIView):
    def get(self, request, format=None):
        django_logout(request)
        messages.success(request, 'Siz cixish etdiniz.')
        return Response({'message':"Siz cixish etdiniz."})

# def login(request):
#     next_page = request.GET.get('next')  # /admin/stories/recipe/1/change/1
#     form = LoginForm()
#     if request.method == 'POST':
#         form = LoginForm(data=request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=email, password=password)
#             if user:
#                 django_login(request, user)
#                 messages.success(request, 'Siz ugurla daxil oldunuz')
#                 if next_page:
#                     return redirect(next_page)
#                 return redirect(reverse_lazy('stories:home'))
#             else:
#                 messages.success(request, 'Daxil etdiyiniz melumatlar yalnisdir')
#     context = {
#         'form': form
#     }
#     return render(request, 'login.html', context)


# @login_required
# def logout(request):
#     django_logout(request)
#     messages.success(request, 'Siz cixis etdiniz')
#     return redirect(reverse_lazy('stories:home'))


@login_required
def change_password(request):
    form = PasswordChangeForm()
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST)
        if form.is_valid():
            old_password = form.cleaned_data["old_password"]
            if not request.user.check_password(old_password):
                messages.error(request, 'Kohne sifre yanlishdir!')
                return redirect(reverse_lazy('accounts:change_password'))
            password1 = form.cleaned_data.get('new_password1')
            password2 = form.cleaned_data.get('new_password2')
            if password1 != password2:
                messages.error(request, 'Yeni sifreler ust-uste dushmur!')
                return redirect(reverse_lazy('accounts:change_password'))
            request.user.set_password(form.cleaned_data["new_password1"])
            request.user.save()
            return redirect(reverse_lazy('stories:home'))
    context = {
        'form': form
    }
    return render(request, 'change_password.html',context)


class UserProfileView(DetailView):
    model = User
    template_name = 'user-profile.html'
    context_object_name = 'user'


class UserEditProfileView(LoginRequiredMixin, UpdateView):
    form_class = EditProfileForm
    model = User
    template_name = 'edit-profile.html'

    def get_object(self):
        return self.request.user

    # def get(self, request, *args, **kwargs):
    #     if not request.user == self.get_object():
    #         raise PermissionDenied
    #     return super(UserEditProfileView, self).get(request, *args, **kwargs)

