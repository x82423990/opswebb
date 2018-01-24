# encoding: utf8
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, loader
from django.views.generic import TemplateView, View, ListView
from con import con
from kubernetes import client, config


def delete_ns(request, ns):
    if request.method == 'POST':
        try:
            config.load_kube_config()
            v1 = client.CoreV1Api()
            NS = client.V1Namespace()
            v1.delete_namespace(body=NS, name=ns)
            data = 'success'
        except IndentationError:
            data = 'error'
        return JsonResponse(data, safe=False)


def delete_dp(request, dp):
    if request.method == 'POST':
        try:
            print(dp)
            data = 'success'
        except IndentationError:
            data = 'error'
        # return JsonResponse(data, safe=False)
        return JsonResponse(data, safe=False)
