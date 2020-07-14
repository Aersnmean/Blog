import json, markdown, datetime
from django.shortcuts import *
from rest_framework.response import Response
from rest_framework import generics
from .serializers import *
from django.utils.decorators import method_decorator


# # 判断是否登录
# def is_login(func):
#     def inner(request, *args, **kwargs):
#         user_account = request.session.get('account', False)
#         if user_account:
#             return func(request, *args, **kwargs)
#         else:
#             print(user_account)
#             return redirect(reverse('blog:page', args=['login']))
#     return inner


# 获取cookie用户信息
def is_jizhu(func):
    def inner(request, *args, **kwargs):
        account = request.COOKIES.get('account', '')
        if account:
            request.session['account'] = account
        return func(request, *args, **kwargs)
    return inner


# # 首页渲染
# def index(request):
#     account = request.COOKIES.get('account', '')
#     if account:
#         request.session['account'] = account
#     return render(request, 'index.html')


# 页面渲染
def render_page(request, page_name):
    return render(request, '{}.html'.format(page_name), {'account': request.session.get('account', '')})


# 用户注册
class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def post(self, request, *args, **kwargs):
        user = User.objects.create(account=request.POST.get('account'), username=request.POST.get('username'), password=request.POST.get('password'))
        request.session['account'] = user.account
        return Response(json.dumps({'status': 200, 'msg': '注册成功'}), status=200)


# 验证手机号是否已注册
class ValidateTel(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def get(self, request, *args, **kwargs):
        try:
            User.objects.get(account=request.GET.get('account'))
        except:
            return Response(json.dumps({'status': 200, 'msg': '手机号可用'}))
        else:
            return Response(json.dumps({'status': 405, 'msg': '手机号已注册'}))


# 用户登录
class Login(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(account=request.GET.get('account'))
        except:
            return Response(json.dumps({'status': 401, 'msg': '用户名或密码错误'}))
        else:
            password = request.GET.get('password')
            if user.password == password:
                is_jizhu = request.GET.get('rem')
                response = Response(json.dumps({'status': 200, 'msg': '登陆成功'}))
                if is_jizhu:
                    response.set_cookie('account', user.account, max_age=1900000)
                else:
                    response.set_cookie('account', '')
                request.session['account'] = user.account
                return response
            else:
                return Response(json.dumps({'status': 405, 'msg': '用户名或密码错误'}))

    def put(self, request, *args, **kwargs):
        try:
            user = User.objects.get(account=request.session['account'])
        except:
            return Response(json.dumps({'status': 401, 'msg': '用户未登录'}))
        else:
            if user.password == request.POST.get('old_password'):
                user.password = request.POST.get('new_password')
                user.save()
                request.session.flush()
                return Response(json.dumps({'status': 200, 'msg': '密码修改成功'}))
            else:
                return Response(json.dumps({'status': 405, 'msg': '原密码错误'}))


def logout(request):
    request.session.flush()
    return HttpResponse(json.dumps({'status': 200, 'msg': '退出登录成功'}), status=200)


# 创建Post
class CPost(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers

    def post(self, request, *args, **kwargs):
        try:
            title = request.POST.get('title')
            body = request.POST.get('title')
            excerpt = request.POST.get('excerpt', '')
            author = User.objects.get(account=request.POST.get('account'))
            Post.objects.create(title=title, body=body, excerpt=excerpt, author=author)
        except:
            return Response(json.dumps({'status': 502, 'msg': '发布失败'}))
        else:
            return Response(json.dumps({'status': 200, 'msg': '发布成功'}))


# 获取所有Post
@method_decorator(is_jizhu, name='dispatch')
class LPost(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = SimPostSerializers

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        for post in posts:
            post.created_time = post.created_time.strftime('%Y-%m-%d')
        return render(request, 'index.html', {'posts': posts, 'new_posts': posts[:3], 'account': request.session.get('account', '')})


# 获取某用户的Post
@method_decorator(is_jizhu, name='dispatch')
class ULPost(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = SimPostSerializers

    def get(self, request, *args, **kwargs):
        account = kwargs.get('account')
        user = User.objects.get(account=account)
        posts = Post.objects.filter(author=user)
        for post in posts:
            post.created_time = post.created_time.strftime('%Y-%m-%d')
        return render(request, 'full-width.html', {'posts': posts, 'account': request.session.get('account', '')})


class RUDPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        post = Post.objects.get(id=post_id)
        post.increase_views()
        reviews = Review.objects.filter(post=post)
        post.body = markdown.markdown(post.body,
                                  extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
        new_posts = Post.objects.all()[:3]
        return render(request, 'single.html', {'post': post, 'new_posts': new_posts, 'reviews': reviews, 'account': request.session.get('account', '')})


# 创建评论
class CReview(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers

    def post(self, request, *args, **kwargs):
        try:
            post_id = kwargs.get('id')
            post = Post.objects.get(id=post_id)
            review = Review.objects.create(text=request.POST.get('text'), post=post, user=User.objects.get(account=request.session['account']))
            review.save()
            post.increase_reviews()
        except Exception as e:
            print(e)
            return Response(json.dumps({'status': 400, 'msg': '评论失败'}), status=400)
        else:
            return Response(json.dumps({'status': 200, 'msg': '评论成功'}), status=200)
