from dashborad.models import Department, Profile
from django.contrib.auth.models import User


d1 = Department(name='salte')
u1 = User.objects.create_user('dashi', 'dashi@41.com')
p1 = Profile(user=u1, phone='112233', title='高级销售', department=d1)

d1.save()

u1.profile.save()

u1.save()