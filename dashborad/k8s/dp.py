# encoding: utf-8
from os import path

import yaml

from kubernetes import client, config


def create_deployment_object(images, tags, rc, envs):

    # 拼装参数
    if '/' in images:
        name = images.split('/')[-1]
    else:
        name = images

    image = images+':'+tags

    container = client.V1Container(
        name=name,
        image='hub.heshidai.com/'+image,
        env=[{'name': 'CONFIG_ENV', 'value': envs}],
        # args=["sleep", "600000"],
        resources=client.V1ResourceRequirements(requests={'cpu': '1000m', 'memory': '1024M'}, limits={'cpu': '1500m', 'memory': '2048M'})
    )

    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": name}),
        spec=client.V1PodSpec(containers=[container],
                              image_pull_secrets=[{'name': 'regsecret'}]
                              ))
    # 指定 specific
    spec = client.ExtensionsV1beta1DeploymentSpec(
        replicas=rc,
        template=template)
    # Instantiate the deployment object

    deployment = client.ExtensionsV1beta1Deployment(
        api_version="extensions/v1beta1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=name),
        spec=spec)

    return deployment


def create_deployment(api_instance, deployment, ns):
    # Create deployement
    api_response = api_instance.create_namespaced_deployment(
        body=deployment,
        namespace=ns)
    print("Deployment created. status='%s'" % str(api_response.status))
    return api_response.status


def update_deployment(api_instance, deployment, images):
    # Update container image
    if '/' in images:
        name = images.split('/')[-1]
    else:
        name = images
    deployment.spec.template.spec.containers[0].image = name
    # Update the deployment
    api_response = api_instance.patch_namespaced_deployment(
        name=name,
        namespace="default",
        body=deployment)
    print("Deployment updated. status='%s'" % str(api_response.status))


def delete_deployment(api_instance, ns, images):
    # Delete deployment
    if '/' in images:
        name = images.split('/')[-1]
    else:
        name = images

    api_response = api_instance.delete_namespaced_deployment(
        name=name,
        namespace=ns,
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
    print("Deployment deleted. status='%s'" % str(api_response.status))


def main():

    config.load_kube_config()

    extensions_v1beta1 = client.ExtensionsV1beta1Api()

    ns = u'bb'.encode('utf-8')
    msg = u'base/nginx'.encode('utf-8')
    tags = u'1.7.9'.encode('utf-8')
    rc = int(u'1'.encode('utf-8'))
    env = u'test'.encode('utf-8')

    deployment = create_deployment_object(tags=tags, images=msg, envs=env, rc=rc)

    # create_deployment(extensions_v1beta1, deployment, ns)
    #
    # update_deployment(extensions_v1beta1, deployment)

    delete_deployment(extensions_v1beta1, ns=ns, images=msg)

if __name__ == '__main__':
    main()