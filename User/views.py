from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            newUser = User(username = username, first_name = first_name, email = email)
            newUser.set_password(password)
            newUser.save()
            login(request, newUser)
            messages.success(request, 'Kaydınız Tamamlanmıştır')

            return redirect('index')
        else:
            context = {
                'form' : form
            }    
            return render(request, 'register.html', context)

    else:
        form = RegisterForm()
        context = {
            'form' : form
        }        

        return render(request, 'register.html', context)

def loginUser(request):
    form = LoginForm(request.POST or None)

    context = {
        'form' :form
    }

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username = username, password = password)

        if user is None:
            messages.warning(request, 'Kullanıcı Adınız veya Parolanız Hatalı')
            return render(request, 'login.html', context)


        messages.success(request, 'Başarılı Giriş')
        login(request, user)
        return redirect('index')

    return render(request, 'login.html', context)    

def logoutUser(request):
    logout(request)

    messages.success(request, 'Çıkış Yaptınız')
    return redirect('index')
