from audioop import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from products.models import Basket
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib import auth
from django.urls import reverse


# Create your views here.
def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, template_name='users/login.html', context=context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request=request, message="Поздравляю с регистрацией!")
            return HttpResponseRedirect(reverse('users:login'))
        else:
            # Debug the form data
            print(form.cleaned_data)
            print(form.errors)
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, template_name='users/registration.html', context=context)


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)
    # baskets = Basket.objects.filter(user=request.user)
    # total_sum = sum(b.sum() for b in baskets)
    # total_quantity = sum(b.quantity for b in baskets)
    # total_sum = 0
    # total_quantity = 0
    # for b in baskets:
    #     total_quantity+=b.quantity
    #     total_sum+=b.sum()
    context = {
        'title': 'Store - Профиль',
        'form': form,
        'baskets': Basket.objects.filter(user=request.user),
    }
    return render(request, template_name='users/profile.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
