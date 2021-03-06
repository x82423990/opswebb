# encoding: utf-8
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, loader
from django.views.generic import TemplateView, View, ListView
from con import con
from kubernetes import client, config
import repitl, dp, string, random
from django.shortcuts import render
from kubernetes.client.rest import ApiException
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator


#
# class PodList(TemplateView):
#
#     template_name = 'k8s/pod.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(PodList, self).get_context_data(**kwargs)
#         # context['userlist'] = User.objects.all()
#         config.load_kube_config()
#         v1 = client.CoreV1Api()
#         ret = v1.list_pod_for_all_namespaces(watch=False)
#
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
#         return super(PodList, self).get(request, *args, **kwargs)


def pod_list(request):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    latest_question_list = v1.list_pod_for_all_namespaces(watch=False)
    template = loader.get_template('k8s/pod.html')
    context = RequestContext(request, {
        'latest_question_list': latest_question_list,
    })
    print(latest_question_list)
    return HttpResponse(template.render(context))


class Nm_list(TemplateView):
    template_name = 'k8s/namespace.html'

    def get_context_data(self, **kwargs):
        config.load_kube_config()
        v1 = client.CoreV1Api()
        # 好像米=前端模板不支持切面,这里把namespace 循环除来=加到nmlist里面
        nm_list = []
        for i in v1.list_namespace(watch=False).items:
            nm_list.append(i.metadata.self_link.split('/')[-1])

        context = super(Nm_list, self).get_context_data(**kwargs)
        context['nm_list'] = nm_list
        return context

    @method_decorator(login_required)
    def get(self, requsete, *args, **kwargs):
        self.request = requsete
        return super(Nm_list, self).get(self, *args, **kwargs)

    def post(self, request):
        ret = {'status': 0}
        name = request.POST.get('name', None)

        if name:
            try:
                # 实例化一个api配置
                config.load_kube_config()
                v1 = client.CoreV1Api()
                # 实例化一个namespace对象
                ns = client.V1Namespace()
                ns.metadata = client.V1ObjectMeta(name=name)

                # 生成namespace
                v1.create_namespace(body=ns)
                print(name)
            except ApiException as e:

                tmp = eval(str(e.body))

                ret['status'] = tmp.get('code')

                ret['msg'] = tmp.get('message')

            return JsonResponse(ret, safe=True)


class Dp_list(TemplateView):
    # 模板渲染
    template_name = 'k8s/dp.html'
    def get_context_data(self, **kwargs):
        config.load_kube_config()
        v1 = client.AppsV1beta2Api()
        context = super(Dp_list, self).get_context_data(**kwargs)
        dp_list = []
        tmp = v1.list_deployment_for_all_namespaces().items

        try:
            for i in tmp:
                ret = {}
                ret['name'] = i.metadata.name
                ret['ns'] = i.metadata.namespace
                ret['replicas'] = i.status.replicas
                ret['available_replicas'] = i.status.available_replicas
                for j in i.spec.template.spec.containers:
                    ret['image'] = j.image
                    if not j.env:
                        ret['env'] = 'no config'
                    else:
                        ret['env'] = j.env[0].value
                dp_list.append(ret)
        except Exception as e:
            print e
        context['dp_list'] = dp_list
        return context

    @method_decorator(login_required)
    def get(self, requsete, *args, **kwargs):
        self.request = requsete
        return super(Dp_list, self).get(self, *args, **kwargs)

class SelectType(View):

    def get(self, request, types):
        if types == 'add':
            return render(request, 'k8s/dpp.html', {'title': 'add dep'})
        if types == 'img':
            a = repitl.get_image_name()
            return JsonResponse(a, safe=False)

        if types == 'pj':
            print(repitl.get_project())

            return JsonResponse(repitl.get_project())

        if types == 'ns':
            config.load_kube_config()
            v1 = client.CoreV1Api()
            nm_list = []
            for i in v1.list_namespace(watch=False).items:
                nm_list.append(i.metadata.self_link.split('/')[-1])
            return JsonResponse(nm_list, safe=False)

        if types == "add_svc":
            return render(request, 'k8s/dpp.html', {'title': 'add svc'})

    def post(self, request, types):
        if types == 'img':
            pj_id = request.POST.get('pid', None)
            print(pj_id)
            a = repitl.get_image_name(project_id=pj_id)
            return JsonResponse(a, safe=False)

        if types == 'tags':
            repo_name = request.POST.get('image')
            tags = repitl.get_tags(repo_name)
            print('tags:', tags)

            return JsonResponse(tags, safe=False)

        if types == 'dep':
            ns = request.POST.get('ns')
            config.load_kube_config()
            v1 = client.AppsV1beta2Api()
            ret = []
            tmp = v1.list_namespaced_deployment(namespace=ns).items
            for i in tmp:
                ret.append(i.metadata.name)
            return JsonResponse(ret, safe=False)

        if types == 'svc':
            ns = request.POST.get('ns')
            # ns = 'default'
            print(ns)
            config.load_kube_config()
            v1 = client.CoreV1Api()
            ret = []
            tmp = v1.list_namespaced_service(ns).items
            for i in tmp:
                ret.append(i.metadata.name)
            return JsonResponse(ret, safe=False)


class Add_Mod_Dp(View):

    @method_decorator(login_required)
    def post(self, request, types):
        if not request.user.is_authenticated():
            return render(request, 'login.html')
        ret = {'status': 0}
        if types == 'add':
            salt = '-'+''.join(random.sample(string.ascii_lowercase, 4))
            if not request.POST.get('ns', None):
                ret['status'] = 404
                ret['msg'] = 'ns不能为空'
                return JsonResponse(ret, safe=True)
            else:
                ns = request.POST.get('ns')
                print(type(ns))

            if not request.POST.get('image', None):
                ret['status'] = 404
                ret['msg'] = 'Image不能为空'
                return JsonResponse(ret, safe=True)
            else:
                msg = request.POST.get('image')
            if not request.POST.get('dp_name', None):
                dp_name = msg.split('/')[-1] + salt
            else:
                dp_name = request.POST.get('dp_name', None) + salt
            if not request.POST.get('tags'):
                ret['status'] = 404
                ret['msg'] = 'tags不能为空'
                return JsonResponse(ret, safe=True)
            else:
                tags = request.POST.get('tags')

            if not request.POST.get('rc', None):
                ret['status'] = 1
                ret['msg'] = 'RC不能为空'
                return JsonResponse(ret, safe=True)
            else:
                rc = int(request.POST.get('rc'))
            if not request.POST.get('env', None):
                ret['status'] = 1
                ret['msg'] = 'Image不能为空'
                return JsonResponse(ret, safe=True)
            else:
                env = request.POST.get('env')
            print(ns, msg, tags, rc, env)
            config.load_kube_config()
            extensions_v1beta1 = client.ExtensionsV1beta1Api()
            try:
                deploy = dp.create_deployment_object(tags=tags, images=msg, rc=rc, envs=env, name=dp_name)
                dp.create_deployment(extensions_v1beta1, deploy, ns=ns)
            except ApiException as e:
                tmp = eval(str(e.body))
                ret['status'] = tmp.get('code')
                ret['msg'] = tmp.get('message')
            return JsonResponse(ret, safe=True)

        if types =='delete':
            ns = request.POST.get('ns_name').encode('utf-8')
            dp_name = request.POST.get('dp_name').encode('utf-8')
            print(ns, dp_name)
            ret = {'status': 0}
            if dp_name is None:
                ret['status'] = 100
                ret['msg'] = 'ns_name or dp_name is None'
                return JsonResponse(ret)
            else:
                try:
                    config.load_kube_config()
                    extensions_v1beta1 = client.ExtensionsV1beta1Api()
                    dp.delete_deployment(extensions_v1beta1, ns=ns, images=dp_name)
                    ret['status'] = 0
                    ret['msg'] = 'ok'
                except Exception as e:
                    ret['status'] = 55
                    ret['msg'] = e
                return JsonResponse(ret)

        if types == 'update':
            ret = {'status': 0}
            dp_name = request.POST.get('dp_name')
            env = request.POST.get('config')
            img = request.POST.get('image')
            ns = request.POST.get('ns')
            tags = request.POST.get('pp')
            rc = request.POST.get('rc')
            # print(dp_name, env, img, tags, ns, rc)
            ret['mgs'] = 'ok'
            config.load_kube_config()
            api = client.ExtensionsV1beta1Api()
            try:
                dp_obj = api.read_namespaced_deployment(name=dp_name, namespace=ns)
                # get dep obj
                deployment = client.ExtensionsV1beta1Deployment(
                    api_version="extensions/v1beta1",
                    kind="Deployment",
                    metadata=client.V1ObjectMeta(name=dp_obj.metadata.name),
                    spec=dp_obj.spec)
                # get env
                tmp = eval(str(deployment.spec.template.spec.containers[0].env[0]))
                tmp['value'] = env
                images = 'hub.heshidai.com/' + img + ':' + tags
                deployment.spec.template.spec.containers[0].image = images
                deployment.spec.replicas = int(rc)
                deployment.spec.template.spec.containers[0].env[0] = tmp

                api.patch_namespaced_deployment(
                    name=dp_obj.metadata.name,
                    namespace=ns,
                    body=deployment)

            except ApiException as e:

                tmp = eval(str(e.body))

                ret['status'] = tmp.get('code')

                ret['msg'] = tmp.get('message')

            return JsonResponse(ret, safe=True)


class Svc_list(TemplateView):
    # def get(self, request, types):
    #
    #     if types == 'list':
    #         config.load_kube_config()
    #         v1 = client.CoreV1Api()
    #         service = v1.list_service_for_all_namespaces().items

    template_name = 'k8s/service.html'

    def get_context_data(self, **kwargs):
        config.load_kube_config()
        v1 = client.CoreV1Api()
        context = super(Svc_list, self).get_context_data(**kwargs)
        svc_list = v1.list_service_for_all_namespaces().items
        context['svc_list'] = svc_list
        return context

    @method_decorator(login_required)
    def get(self, requsete, *args, **kwargs):
        self.request = requsete
        return super(Svc_list, self).get(self, *args, **kwargs)


class Add_Mod_svc(View):
    def post(self, request, types):
        if not request.user.is_authenticated():
            return render(request, 'login.html')
        if types == 'add':

            ret = {'status': 0}

                #
                # # name = request.POST.get('svc_name', None).encode("utf-8")
                # # ns = request.POST.get('ns', None).encode("utf-8")
                # # labels = request.POST.get('label', None).encode("utf-8")
                # # if not labels:
                # #     ret['msg'] = "标签不能为空"
                # #     ret['status'] = 121
                # #     return JsonResponse(ret, safe=True)
                # # if not name:
                # #     name = labels
                # # ports = request.POST.get('port', None).encode("utf-8")
                # # target = request.POST.get('target', None).encode("utf-8")
                #

            if request.POST.get('ns'):
                ns = request.POST.get('ns').encode()
                # print(ns)
            else:
                ret['msg'] = "ns不能为空"
                ret['status'] = 123
                return JsonResponse(ret, safe=True)

            if request.POST.get('label'):
                labels = request.POST.get('label').encode()
                print(labels)
            else:
                ret['msg'] = "label不能为空"
                ret['status'] = 124
                return JsonResponse(ret, safe=True)

            if request.POST.get('svc_name'):
                name = request.POST.get('svc_name').encode()
                print(name)
            else:
                name = labels

            if request.POST.get('port'):
                ports = int(request.POST.get('port').encode())

            else:
                ret['msg'] = "port不能为空"
                ret['status'] = 125
                return JsonResponse(ret, safe=True)

            if request.POST.get('target'):
                target = int(request.POST.get('target').encode())
            else:
                ret['msg'] = "target不能为空"
                ret['status'] = 126
                return JsonResponse(ret, safe=True)

                # print(type(ns))
                # print(ns)
            print(name, ns, labels, ports, target)
            print(type(name), type(ns), type(labels), type(ports), type(target))
            # name = '2048'
            # ns = 'bb'
            # labels = '2048'
            # ports = 80
            # target = 80
            try:
                config.load_kube_config()
                api_instance = client.CoreV1Api()
                service = client.V1Service()
                service.api_version = "v1"
                service.kind = "Service"
                service.metadata = client.V1ObjectMeta(name=name)
                spec = client.V1ServiceSpec()
                spec.selector = {"app": labels}
                spec.ports = [client.V1ServicePort(protocol="TCP", port=ports, target_port=target)]
                service.spec = spec
                api_instance.create_namespaced_service(namespace=ns, body=service)
                ret['msg'] = "服务创建成功"

            except ApiException as e:

                tmp = eval(str(e.body))

                ret['status'] = tmp.get('code')

                ret['msg'] = tmp.get('message')

            return JsonResponse(ret, safe=True)

        if types == 'del':
            ret = {'status': 0}
            ns = request.POST.get('ns_name')
            svc_name = request.POST.get('svc_name')
            print(svc_name, ns)
            try:
                config.load_kube_config()
                api_instance = client.CoreV1Api()
                api_instance.delete_namespaced_service(name=svc_name, namespace=ns)

            except ApiException as e:
                tmp = eval(str(e.body))
                ret['status'] = tmp.get('code')
                ret['msg'] = tmp.get('message')
            return JsonResponse(ret, safe=True)


class Ing_list(TemplateView):
    template_name = 'k8s/ingress.html'

    def get_context_data(self, **kwargs):
        configuration = config.load_kube_config()
        api_instance = client.ExtensionsV1beta1Api(client.ApiClient(configuration))

        ret = []
        for i in api_instance.list_ingress_for_all_namespaces().items:
            print(i.metadata.namespace)
            ret.append({'name': i.metadata.name, 'namespaces': i.metadata.namespace, \
                        'svc_name': i.spec.rules[0].http.paths[0].backend.service_name, \
                        'svc_port': i.spec.rules[0].http.paths[0].backend.service_port, \
                        'host': i.spec.rules[0].host})
            print(ret)
        context = super(Ing_list, self).get_context_data(**kwargs)
        context['ing_list'] = ret
        return context

    @method_decorator(login_required)
    def get(self, requsete, *args, **kwargs):
        self.request = requsete
        return super(Ing_list, self).get(self, *args, **kwargs)


class Ing_Add_Mod(View):

    def post(self, request, types):
        if types == 'add':
            ret = {'status': 0}
            ing_name = request.POST.get('ing_name')
            ns = request.POST.get('ns').encode()
            svc_name = request.POST.get('label').encode()
            port = request.POST.get('port').encode()
            host = request.POST.get('host', None)
            if not ing_name:
                ing_name = svc_name
            if not host:
                host = ing_name+'.cd.maijinbei.cn'
            print(ing_name, ns, svc_name, port, host)

            config.load_kube_config()
            body = client.V1beta1Ingress()
            body.api_version = 'extensions/v1beta1'
            body.kind = 'Ingress'
            bakend = client.V1beta1IngressBackend(service_name=svc_name, service_port=80)
            paths = [client.V1beta1HTTPIngressPath(backend=bakend)]

            htp = client.V1beta1HTTPIngressRuleValue(paths=paths)
            rules = [client.V1beta1IngressRule(host=host, http=htp)]

            body.metadata = client.V1ObjectMeta(name=ing_name)
            body.spec = client.V1beta1IngressSpec(rules=rules)
            api = client.ExtensionsV1beta1Api()
            try:
                api.create_namespaced_ingress(ns, body)

            except ApiException as e:
                tmp = eval(str(e.body))
                ret['status'] = tmp.get('code')
                ret['msg'] = tmp.get('message')
            return JsonResponse(ret, safe=True)

        if types == 'del':

            ret = {'status': 0}
            ing_name = request.POST.get('ing_name').encode()
            ns = request.POST.get('ns_name').encode()
            print(ing_name, ns)
            config.load_kube_config()
            try:
                ad = client.V1DeleteOptions(api_version='extensions/v1beta1')
                client.ExtensionsV1beta1Api().delete_namespaced_ingress(namespace=ns, name=ing_name, body=ad)
            except ApiException as e:
                print("Exception when calling ExtensionsV1beta1Api->create_namespaced_ingress: %s\n" % e)
                ret['status'] = 12
                ret['msg'] = e
                return JsonResponse(ret, safe=True)
            return JsonResponse(ret, safe=True)

        if types == 'update':
            ret = {'status': 0}
            ing_name = request.POST.get('ing_name', None)
            m_ns = request.POST.get('m_ns', None)
            m_port = request.POST.get('m_port', None)
            m_host = request.POST.get('m_host', None)
            m_label = request.POST.get('m_label', None)
            config.load_kube_config()
            api = client.ExtensionsV1beta1Api()
            try:
                ing_obj = api.read_namespaced_ingress(ing_name, m_ns)
                ing_obj.spec.rules[0].http.paths[0].backend.service_name = m_label
                ing_obj.spec.rules[0].http.paths[0].backend.service_port = int(m_port)
                ing_obj.spec.rules[0].host = m_host
                api.patch_namespaced_ingress(ing_name, m_ns, ing_obj)
                ret['msg'] = 'succeed'
            except ApiException as e:
                tmp = eval(str(e.body))
                ret['status'] = tmp.get('code')
                ret['msg'] = tmp.get('message')
            return JsonResponse(ret, safe=True)


class pr_test(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, "public/index.html")







