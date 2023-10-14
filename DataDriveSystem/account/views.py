from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserRegistrationForm
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
# Create your views here.


def index(request):
    return render(request, 'index.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')

    else:
        form = UserRegistrationForm()

    return render(request, 'account/register.html', {'form': form})

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return render(request, 'folder/file_list.html')

    else:
        form = AuthenticationForm()

    return render(request, 'account/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return render(request,'account/logout.html')



