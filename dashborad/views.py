# coding:utf8
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, QueryDict
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View


# Create your views here.


class Log_In_Out(View):

    def get(self, request):
        return render(request, 'login.html', {'title': 'rebbot 晕为'})

    def post(self, request):
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            ret = {'status': 0}
            # 验证用户名密码
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    ret['nexturl'] = '/'
                else:
                    ret['status'] = 1
                    ret['errmsg'] = '用户被禁用'

            else:
                ret['status'] = 2
                ret['errmsg'] = 'err'
                print ret
            return JsonResponse(ret, safe=True)

class LogOut(View):

    def get(self, request):
        logout(request)
        return HttpResponse('用户退出chenggong')


class IndexView(View):
    def get(self, request):
        return render(request, "public/index.html")