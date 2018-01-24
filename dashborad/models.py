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
    status = models.IntegerField()
    loads = models.CharField(max_length=20)

    class Meta:
        db_table = 'server'
        # permissions = (
        #     ('view_server', 'view servers info'),   # 添加一个权限到数据库中的auth_permission表中
        #     # 添加权限
        #     #  user.user_permissions.add(权限对象)
        #     # 权限对象  Permission.objects.get(pk=28)
        #     # 权限列表  Permission.objects.filter(pk=28)
        #     # 清空权限 user.user_permissions = []
        #     # 检查用户是否拥有权限 has_perm来检查用户使用有权限
        #     # 检查用户是否拥有权限 has_perm来检查用户使用有权限
        # # )
        # permissions = (
        #     ('view_server', '访问服务器信息'),
        #     ('view_user_list', '访问用户列表')

        # 授权
        # from django.contrib.auth.models import Permission, ContentType
        # Permission()
        # p
        # .name = '访问用户列表'
        #
        # p.content_type = ct
        #
        # p.codename = 'view_user_list'
        #
        # p.save()


# class Crontab(models.Model):
#     details = models.CharField(max_length=256)
#     host = models.ForeignKey(Server, null=False)


class test(models.Model):
    a = models.CharField(max_length=21)
    on_delete = models.DO_NOTHING,


class IDC(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = 'idc'


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
    objects = models.Manager()  # 引用的时候发现没有这个属性,临时添加的.


    class Meta:
        db_table = 'user_profile'
        default_related_name = 'profile'
# # 一个一对一的例子
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




    #     from django.db import models
    #
    #     class Place(models.Model):
    #         name = models.CharField(max_length=50)
    #         address = models.CharField(max_length=80)
    #
    #         def __str__(self):  # __unicode__ on Python 2
    #             return "%s the place" % self.name
    #
    #     class Restaurant(models.Model):
    #         place = models.OneToOneField(Place, primary_key=True)
    #         serves_hot_dogs = models.BooleanField(default=False)
    #         serves_pizza = models.BooleanField(default=False)
    #
    #         def __str__(self):  # __unicode__ on Python 2
    #             return "%s the restaurant" % self.place.name
    #
    #     class Waiter(models.Model):
    #         restaurant = models.ForeignKey(Restaurant)
    #         name = models.CharField(max_length=50)
    #
    #         def __str__(self):  # __unicode__ on Python 2
    #             return "%s the waiter at %s" % (self.name, self.restaurant)
    #
    #     以下是可以使用Python
    #     API执行查询操作的示例。
    #
    #     创建几个Places对象：
    #
    #     >> > p1 = Place(name='Demon Dogs', address='944 W. Fullerton')
    #     >> > p1.save()
    #     >> > p2 = Place(name='Ace Hardware', address='1013 N. Ashland')
    #     >> > p2.save()
    #     创建Restaurant对象。将“父”对象的ID作为此对象的ID：
    #
    #     >> > r = Restaurant(place=p1, serves_hot_dogs=True, serves_pizza=False)
    #     >> > r.save()
    #     从Restaurant对象可以访问它的Place：
    #
    #     >> > r.place
    #     < Place: Demon
    #     Dogs
    #     the
    #     place >
    #     从Place对象可以访问它的Restaurant(如果存在的话)：
    #
    #     >> > p1.restaurant
    #     < Restaurant: Demon
    #     Dogs
    #     the
    #     restaurant >
    #     p2没有相关的餐厅：
    #
    #     >> > from django.core.exceptions import ObjectDoesNotExist
    #     >> > try:
    #         >> > p2.restaurant
    #     >> > except ObjectDoesNotExist:
    #     >> > print("There is no restaurant here.")
    #     There is no
    #     restaurant
    #     here.
    #     您还可以使用hasattr来避免异常捕获的需要：
    #
    #     >> > hasattr(p2, 'restaurant')
    #     False
    #     使用赋值表示Place。由于place字段是Restaurant表的主键, 所以这里的save()
    #     操作会创建一个新的Restaurant对象：
    #
    #     >> > r.place = p2
    #     >> > r.save()
    #     >> > p2.restaurant
    #     < Restaurant: Ace
    #     Hardware
    #     the
    #     restaurant >
    #     >> > r.place
    #     < Place: Ace
    #     Hardware
    #     the
    #     place >
    #     再次指定Place，这次使用相反的方向进行赋值：
    #
    #     >> > p1.restaurant = r
    #     >> > p1.restaurant
    #     < Restaurant: Demon
    #     Dogs
    #     the
    #     restaurant >
    #     请注意，必须先保存对象，然后才能将其分配给一对一关系。例如，使用未保存的Place创建Restaurant会产生ValueError：
    #
    #     >> > p3 = Place(name='Demon Dogs', address='944 W. Fullerton')
    #     >> > Restaurant(place=p3, serves_hot_dogs=True, serves_pizza=False)
    #     Traceback(most
    #     recent
    #     call
    #     last):
    #     ...
    #     ValueError: 'Cannot assign "<Place: Demon Dogs>": "Place" instance isn'
    #     t
    #     saved in the
    #     database.
    #     '
    #     >> > p.restaurant = Restaurant(place=p, serves_hot_dogs=True, serves_pizza=False)
    #     Traceback(most
    #     recent
    #     call
    #     last):
    #     ...
    #     ValueError: 'Cannot assign "<Restaurant: Demon Dogs the restaurant>": "Restaurant" instance isn'
    #     t
    #     saved in the
    #     database.