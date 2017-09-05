# coding:utf8
from django.utils.decorators import method_decorator
from  django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import  TemplateView, View, ListView
from django.contrib.auth.models import Group, User, Permission
from django.http import JsonResponse, HttpResponse
from django.core import serializers
import logging

logger = logging.getLogger('opsweb')

class GroupListView(ListView):
    model = Group
    template_name = 'user/userlist1.html'

    def post(self, request):
        ret = {'status': 0}
        name = request.POST.get('name', None)
        print name
        if name:
            try:
                print name
                group = Group()
                group.name = name
                group.save()
            except Exception as e:
                ret['msg'] = e.args
                ret['status'] = 2
        return JsonResponse(ret, safe=True)


class GroupView(View):

    # 获取用户组信息

    def get(self, request):
        uid = request.GET.get('uid')
        # ret = {'status': 0}
        # try:
        #     Group.objects.all()
        user = User.objects.get(pk=uid)
        groups = [i for i in Group.objects.all() if i not in user.groups.all()]
        print groups
        return HttpResponse(serializers.serialize('json', groups), content_type='application/json')


class UserGroup(View):
    # 将用户添加到指定组
    def post(self, request):
        ret = {'status': 0}
        gid = request.POST.get('gid')
        uid = request.POST.get('uid')
        try:
            user = User.objects.get(pk=uid)
        except Exception as e:
            logger.error(e)
            ret['status'] = 1
            ret['msg'] = e
            return JsonResponse(ret, safe=True)
        try:
            group = Group.objects.get(pk=gid)
        except Exception as e:
            logger.error(e)
            ret['status'] = 1
            ret['msg'] = e
            return JsonResponse(ret, safe=True)

        user.groups.add(group)
        return JsonResponse(ret, safe=True)