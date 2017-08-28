# coding:utf8
from django.views.generic import TemplateView, View, ListView
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from dashborad.models import Department, Server


class UserListView(TemplateView):
    template_name = 'user/wuser.html'

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        # context['userlist'] = User.objects.all()
        userlist = User.objects.all()
        # 获取所有的用户列表对象
        paginator = Paginator(userlist, 2)
        page = self.request.GET.get('page', 1)
        print page
        try:
            page_obj = paginator.page(page)
        except EmptyPage:
            page_obj = paginator.page(1)
        print page_obj.object_list
        context['page_obj'] = page_obj
        CountPage = page_obj.paginator.page_range
        if page_obj.number < 6:
            CurPage = 6
        else:
            CurPage = page_obj.number
        ppaa = CountPage[CurPage-6:CurPage+4]
        context['views_page'] = ppaa
        return context

    def get(self, request, *args, **kwargs):
        self.request = request
        return super(UserListView, self).get(request, *args, **kwargs)


class LW(ListView):
    template_name = 'user/wuser.html'
    model = User
    paginate_by = 8


class Modify_status(View):
    def post(self, resquest):
        ret = {'status': 0}
        user_id = resquest.POST.get('user_id', None)
        print user_id
        try:
            user = User.objects.get(pk=user_id)
            print user
            if user.is_active:
                user.is_active = False
            else:
                user.is_active= True
            user.save()
        except User.DoesNotExist:
            ret['status'] = 1
            print ret
            ret['errmsg'] = 'User is not exist'
            print ret['errmsg']
        return JsonResponse(ret, safe=True)


class ModifyDepartmentView(TemplateView):
    template_name = 'user/department.html'

    def get_context_data(self, **kwargs):
        context = super(ModifyDepartmentView, self).get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        context['user_obj'] = User.objects.get(pk=self.request.GET.get('user', None))
        return context

    def get(self, requsete, *args, **kwargs):
        self.request = requsete
        return super(ModifyDepartmentView, self).get(self, *args, **kwargs)

    def post(self, request):
        print request.POST
        return HttpResponse('')
