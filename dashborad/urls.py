from django.conf.urls import url, include
from . import views
from . import user, server
from dashborad.user import group
from dashborad import cron
urlpatterns = [
    # url(r'^login/', views.login_view),
    url(r'^login/', views.Log_In_Out.as_view()),
    url(r'^logout/', views.LogOut.as_view()),
    url(r'^$', views.IndexView.as_view()),
    # url(r'^user/userlist/', user.UserListView.as_view()),
    url(r'^user/userlist/', user.LW.as_view()),
    url(r'^user/modify/', user.Modify_status.as_view()),
    url(r'^user/modp/', user.ModifyDepartmentView.as_view()),
    url(r'^user/mp', user.ModifyPhoneView.as_view()),
    url(r'^permissions/', include([
        url(r'^none/$', views.permit),
    ])),
    url(r'^group/', include([
        url(r'list/$', group.GroupListView.as_view()),
        url(r'^$', group.GroupView.as_view()),
        url(r'^usergroup/', group.UserGroup.as_view()),
    ])),
    url(r'^server/', include([
        url(r'^list/$', server.GroupList.as_view()),
        url(r'add_server', server.AddServer.as_view())
    ])),
    url(r'^cron/', include([
        url(r'^list/$', cron.CronManger.as_view()),
        url(r'^view/$', cron.CronView.as_view()),

    ]))

]