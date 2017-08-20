from django.conf.urls import url
from . import views
from . import user

urlpatterns = [
    # url(r'^login/', views.login_view),
    url(r'^login/', views.Log_In_Out.as_view()),
    url(r'^logout/', views.LogOut.as_view()),
    url(r'^$', views.IndexView.as_view()),
    # url(r'^user/userlist/', user.UserListView.as_view()),
    url(r'^user/userlist/', user.LW.as_view()),
    url(r'^user/modify/', user.Modify_status.as_view()),
]