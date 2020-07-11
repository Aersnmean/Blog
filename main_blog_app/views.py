import json
from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework_mongoengine import generics
from .serializers import *


# 首页渲染
def index(request):
    return render(request, 'index.html')


# 页面渲染
def render_page(request, page_name):
    return render(request, '{}'.format(page_name))


# 用户注册
class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers


# 验证手机号是否已注册
class ValidateUsername(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def get(self, request, *args, **kwargs):
        try:
            User.objects.get(account=request.GET.get('name'))
        except:
            return Response(json.dumps({'status': 200, 'msg': '手机号可用'}))
        else:
            return Response(json.dumps({'status': 405, 'msg': '手机号已注册'}))


class Login(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.GET.get('username'))
        except:
            return Response(json.dumps({'status': 405, 'msg': '用户名或密码错误'}))
        else:
            password = request.GET.get('password')
            if user.password == password:
                request.session['user'] = user.username
                return Response(json.dumps({'status': 200, 'msg': '登陆成功'}))
            else:
                return Response(json.dumps({'status': 405, 'msg': '用户名或密码错误'}))


class OneUser(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    lookup_field = 'name'

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=kwargs.get('name'))
        except:
            return Response(json.dumps({'status': 405, 'msg': '用户名信息不存在'}))
        else:
            tel = user.tel[:3]+'****'+user.tel[7:]
            password = '*'*len(user.password)
            return Response(json.dumps({'status': 405, 'msg': '用户名信息不存在', 'tel': tel, 'password': password}))

    def put(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=kwargs.get('name'))
        except:
            return Response(json.dumps({'status': 405, 'msg': '用户名信息不存在'}))
        else:
            if request.POST.get('old_password') == user.password:
                user.password = request.POST.get('new_password')
                user.save()
                return Response(json.dumps({'status': 200, 'msg': '修改成功'}))
            else:
                return Response(json.dumps({'status': 400, 'msg': '原密码错误'}))


def logout(request):
    del request.session['user']
    return HttpResponse(status=200)


def getlog(request):
    return HttpResponse(request.session['user'], status=200)


