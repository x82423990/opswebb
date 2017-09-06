from dashborad.models import Department, Profile
from django.contrib.auth.models import User

# 新增
d1 = Department(name='salte')
u1 = User.objects.create_user('dashi', 'dashi@41.com')
p1 = Profile(user=u1, phone='112233', title='高级销售', department=d1)


u1.profile.save()

u1.save()

# 查询新增

d2 = Department(name='dev')
u2 = User.objects.get(pk=2)

p2 = Profile(user=u2, department=d2)