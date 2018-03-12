from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from EasyCmdb import forms
from django.http import JsonResponse
from utils.response import BaseResponse


def acclogin(request):
    if request.method == 'POST':
        form_obj = forms.AccloginForm(request.POST)
        if form_obj.is_valid():
            user = authenticate(**form_obj.cleaned_data)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    error_message = '该邮箱无权登录'

            else:
                error_message = '邮箱或密码错误'
        else:
            error_message = '邮箱或密码不能为空'
        return render(request, 'acclogin.html', {'form_obj': form_obj, 'error_message': error_message})
    elif request.method == 'GET':
        form_obj = forms.AccloginForm()
        return render(request, 'acclogin.html', {'form_obj': form_obj})


def acclogout(request):
    logout(request)
    return redirect('/login.html')


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def user_info(request):
    if request.method == 'POST':
        response = BaseResponse()
        form_obj = forms.UserInfoForm(request.POST)
        if form_obj.is_valid():
            password = form_obj.cleaned_data['password1']
            request.user.set_password(password)
            request.user.save()
        else:
            response.status = False
            response.message = '密码修改失败'
        return JsonResponse(response.__dict__)
    return render(request, 'user_info.html')
