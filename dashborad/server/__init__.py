# coding:utf8
from django.utils.decorators import method_decorator
from  django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import  TemplateView, View, ListView
from django.contrib.auth.models import Group, User, Permission
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core import serializers
import logging
from dashborad.models import Server



class GroupList(ListView):

    template_name = 'public/server_list.html'
    model = Server
    paginate_by = 10



class AddServer(View):
    def post(self, request):
        hostname = request.POST.get('hostname')
        ip = request.POST.get('address')
        status = request.POST.get('status')
        print hostname, ip, status
        try:
            Server.objects.create(hostname=hostname, ip=ip, status=str(status))
        except Exception as e:
            print e
        return HttpResponseRedirect('/server/list')
        # return HttpResponse(request)

    def delete(self, request):

        pass

    def update(self, request):

        pass


