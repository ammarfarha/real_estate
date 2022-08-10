from django.shortcuts import render


def client_signup(request):
    return render(request, 'register.html')


def developer_signup(request):
    return render(request, 'signup.html')


def sign_in(request):
    return render(request, 'signup.html')


def sign_out(request):
    return render(request, 'signup.html')


def forget_password(request):
    return render(request, 'signup.html')
