from kubernetes import client, config


def con():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    return v1


if __name__ == '__main__':
    con()