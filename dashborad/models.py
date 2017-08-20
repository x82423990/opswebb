from django.db import models

# Create your models here.


class Server(models.Model):
    hostname = models.CharField(max_length=32, unique=True)
    ip = models.CharField(max_length=15, unique=True)
    cpu = models.CharField(max_length=50, null=True)
    mem = models.CharField(max_length=50)
    disk = models.CharField(max_length=50)
    sn = models.CharField(max_length=60)
    idc = models.CharField(max_length=50)
    ipinfo = models.CharField("[{'eth0': '192.168.168.1', 'mac_addr': 'dsfsd'}]", max_length=50)
    product = models.CharField(max_length=50)
    remark = models.TextField(default='')
    class Meta:
        db_table = 'server'

