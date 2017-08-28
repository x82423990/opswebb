# coding:utf8
from django.db import models
from django.contrib.auth.models import User
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


class Department(models.Model):
    name = models.CharField(max_length=11, null=True)
    objects = models.Manager()  # 引用的时候发现没有这个属性,临时添加的.

    class Meta:
        db_table = 'department'


class Profile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=11)
    department = models.CharField(max_length=32)
    title = models.CharField(max_length=32)
    department = models.ForeignKey(Department, null=True)

    class Meta:
        db_table = 'user_profile'
        default_related_name = 'profile'


    # user = models.OneToOneField(User) 关联一对一关联
    #
    # user = User.objects.create_user('rock11', 'rock@51@.com', '123')
    # user_profile = Profile
    #
    # user_profile.user = user
    # user_profile.phone = '123'
    # user_profile.title = '云维'
    # user_profile.save()
    # 查询
    #
    # user = User.objects.get(username='rock')
    # user.profile.title


    # 同步数据
    # python manage.py makemigrations dashborad
    # python manage.py migrate dashborad
    # python manage.py shell
    # 如果出错,
        # python manage.py makemigrations dashborad --fake  让这个步骤强行成功


    # 添加数据
    #   from dashborad.models import Department
    #   d = Department(name='devops')
    #   d.save()

    # 或者 Department.objects.create(name='dev'), 添加一个一个开发部.

