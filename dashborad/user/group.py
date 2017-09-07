# coding:utf8
from django.utils.decorators import method_decorator
from  django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import  TemplateView, View, ListView
from django.contrib.auth.models import Group, User, Permission
from django.http import JsonResponse, HttpResponse, QueryDict
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
        print uid
        # ret = {'status': 0}
        # try:
        #     Group.objects.all()
        user = User.objects.get(pk=uid)
        groups = [i for i in Group.objects.all() if i not in user.groups.all()]
        group = Group.objects.all()
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

    def get(self, request):
        gid = request.GET.get('gid', None)
        try:
            # groups = Group.objects.get(pk=gid)
            groups = Group.objects.get(pk=gid)
            groups = [{'id': i.id, 'name': i.username, 'email': i.email} for i in groups.user_set.all()]
            print groups
            return JsonResponse(groups, safe=False)
            # return JsonResponse([], safe=False)
        except:
            return JsonResponse([], safe=False)

    def delete(self, request):
        ret = {'status':0}
        res_obj = QueryDict(request.body)
        uid = res_obj.get('uid')
        gid = res_obj.get('gid')
        print uid, gid
        try:
            user = User.objects.get(pk=uid)
            group = Group.objects.get(pk=gid)
            group.user_set.remove(user)
        except Exception as e:
            ret['status'] = 1
            ret['msg'] = e.args
        return JsonResponse(ret)

