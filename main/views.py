import hashlib
from django.http import HttpResponse
from django.shortcuts import render, redirect
from . models import User
from . forms import UserForm

def index(request):
    return render(request, 'main/index.html', {})

def base(request):
    return render(request, 'main/base.html', {})

def signup(request):
    form = UserForm()
    if request.POST:
        passw = request.POST.get('password')
        username = request.POST.get('username')
        password = hashlib.md5(passw.encode('utf-8')).hexdigest()
        token = request.POST.get('csrfmiddlewaretoken')
        form = UserForm({'csrfmiddlewaretoken': [token], 'username': [
                        username], 'password': [password]})
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'main/signup.html', {'form': form})

def login(request):
    form = UserForm()
    user = User.objects.all()
    if request.POST:
        username = request.POST.get('username')
        try:
            user = user.get(username=[username])
            users = user
        except ValueError:
            return HttpResponse('<b>Usuario nao Existe<b/>')
        if user:
            password = request.POST.get('password')
            password = hashlib.md5(password.encode('utf-8')).hexdigest()
            try:
                password = User.objects.all().get(password=[password])
            except ValueError:
                return HttpResponse('<b>A senha digitada esta errada<b/>')
            if password.password == users.password:
                return redirect('index')
            else:
                return HttpResponse('<b>A senha digitada esta errada<b/>')
        else:
            return HttpResponse('<b>Usuario nao Existe<b/>')
    return render(request, 'main/login.html', {'form': form})
