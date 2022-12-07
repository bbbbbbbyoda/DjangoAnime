from django.shortcuts import render

from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from .models import MyUser


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()

    return render(request, template_name="account/login.html", context={"login_form": form})


def logout_user(request):
    logout(request)
    return redirect('index')


def sign_up(request):

    if request.method == 'POST':
        user_email = request.POST.get('email')
        user_login = request.POST.get('login')
        user_date_of_birth = request.POST.get('date_of_birth')
        user_password = request.POST.get('password')

        MyUser.objects.create_user(email=user_email, login=user_login, date_of_birth=user_date_of_birth, password=user_password).save()


    return render(request, template_name='account/sign-up.html')











