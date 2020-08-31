from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm

def home_view(request):
    
    context = {

    }
    return render(request,'home.html',context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def login_view(request):
    if request.method=='POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.data.get('username')
            password = form.data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    return HttpResponseRedirect(request.GET.get('next'))
                else:
                    return HttpResponseRedirect(reverse('home'))
            else:
                messages.error(request,'Oops seems Username or Password is wrong!')
                return HttpResponseRedirect(request.path)     
    else:
        form = LoginForm()
    context = {
        'form':form,
    }
    return render(request,'login.html',context)