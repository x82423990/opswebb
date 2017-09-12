# coding:utf8
import paramiko, re
import sys
from .callback import *
from .inventory import *
from .runner import *
from django.views.generic import TemplateView, ListView, View
from dashborad.models import Server
from django.http import HttpResponse, JsonResponse
from .runner import *
reload(sys)
sys.setdefaultencoding('utf-8')


class CronManger(ListView):
    template_name = 'public/data_table.html'
    model = Server
    context_object_name = 'ser_obj'


class CronView(View):
    def get(self, request):
        s_id = request.GET.get('id')
        obj = Server.objects.get(pk=s_id)
        res = [{
            'ip': obj.ip,
            'name': obj.hostname,
            'private_key': '/Users/xieyifan/Documents/keys/newjump',
            'username': 'ubuntu',
            'port': 22
        }, ]
        task = (('shell', 'crontab -l'),)
        hoc = AdHocRunner(hosts=res)
        hoc.results_callback = CommandResultCallback()
        ret = hoc.run(task)
        try:
            rets = hoc.run(task)
            ret = ret.get('contacted').get('10.0.0.93')[0].get('stdout')
        except Exception as e:
            print e.args
        return JsonResponse(ret)



