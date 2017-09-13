# coding:utf8
from django.views.generic import TemplateView, View, ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage
from dashborad.models import Department, Profile
from django.conf import settings
from opsweb.settings import TEMPLATE_JUMP
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.core import serializers


# class UserListView(TemplateView):
#     template_name = 'user/wuser.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(UserListView, self).get_context_data(**kwargs)
#         # context['userlist'] = User.objects.all()
#         userlist = User.objects.all()
#         # 获取所有的用户列表对象
#         paginator = Paginator(userlist, 2)
#         page = self.request.GET.get('page', 1)
#         print page
#         try:
#             page_obj = paginator.page(page)
#         except EmptyPage:
#             page_obj = paginator.page(1)
#         print page_obj.object_list
#         context['page_obj'] = page_obj
#         CountPage = page_obj.paginator.page_range
#         if page_obj.number < 6:
#             CurPage = 6
#         else:
#             CurPage = page_obj.number
#         ppaa = CountPage[CurPage-6:CurPage+4]
#         context['views_page'] = ppaa
#         return context
#
#     def get(self, request, *args, **kwargs):
#         self.request = request
#         return super(UserListView, self).get(request, *args, **kwargs)


class LW(ListView):
    template_name = 'user/wuser.html'
    model = User
    paginate_by = 10

    @method_decorator(login_required)
    @method_decorator(permission_required('auth.view_user_list', login_url=settings.TEMPLATE_403))
    def get(self,  request, *args, **kwargs):
        return super(LW, self).get(request, *args, **kwargs)


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
                user.is_active = True
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
        context['user_obj'] = get_object_or_404(User, id=self.request.GET.get('user', None))    # 这个方法好,直接在获取参数的时候判断是否存在
        return context

    @method_decorator(login_required)
    @method_decorator(permission_required('dashborad.change_department', login_url=settings.TEMPLATE_403))
    def get(self, requsete, *args, **kwargs):
        self.request = requsete
        return super(ModifyDepartmentView, self).get(self, *args, **kwargs)

    @method_decorator(login_required)
    @method_decorator(permission_required('dashborad.change_department', login_url=settings.TEMPLATE_403))
    def post(self, request):
        user_id = request.POST.get('user', None)
        dpart_id = request.POST.get('department', None)
        if not user_id or not dpart_id:
            raise Http404
        try:
            use_obj = User.objects.get(pk=user_id)
            depart_obj = Department.objects.get(pk=dpart_id)
        except:
            raise Http404
        else:
            try:
                use_obj.profile.department = depart_obj
                use_obj.profile.save()
            except:
                # raise Http404
                p = Profile(user=use_obj, department=depart_obj)
                p.user.save()
                p.department.save()
                p.save()
                return redirect('/user/userlist/')
            else:
                return redirect('/user/userlist/')


class ModifyPhoneView(TemplateView):
    template_name = 'user/mp.html'

    def get_context_data(self, **kwargs):
        context = super(ModifyPhoneView, self).get_context_data(**kwargs)
        context['user_obj'] = get_object_or_404(User, pk=self.request.GET.get('user', None))
        return context

    def get(self, request, *args, **kwargs):
        self.requset = request
        return super(ModifyPhoneView, self).get(self, *args, **kwargs)

    def post(self, request):
        user_id = request.POST.get('user', None)
        phone_num = request.POST.get('pnum', None)
        if not user_id or not phone_num:
            raise Http404
        try:
            #   保存模型
            user_obj = User.objects.get(pk=user_id)
            user_obj.profile.phone = phone_num
            user_obj.profile.save()
            print settings.TEMPLATE_JUMP
            return render(request, settings.TEMPLATE_JUMP, {"status": 0, "next_url": '/user/userlist/'})
            # return HttpResponse('ok')
        except:
            return HttpResponse('err')
        # else:
        #     return redirect('/user/userlist/')
        #













# In [36]: user.user_permissions.add(Permission.objects.get(pk=28))
# In [38]: user.user_permissions.remove(Permission.objects.get(pk=28))

# d2 = Department(name='dev')
# u2 = User.objects.get(pk=2)
#
# p2 = Profile(user=u2, department=d2)


