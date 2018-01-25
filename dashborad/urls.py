from django.conf.urls import url, include
from . import views
from . import user, server, k8s
from dashborad.user import group
from dashborad.k8s import deletes
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
        url(r'^per/', group.PermissionList.as_view()),

    ])),
    url(r'^server/', include([
        url(r'^list/$', server.GroupList.as_view()),
        url(r'add_server', server.AddServer.as_view())
    ])),
    url(r'^k8s/', include([
        url(r'^podlist/$', k8s.pod_list),
        url(r'^nmlist/$', k8s.Nm_list.as_view()),
        url(r'^delete/ns/(?P<ns>.*)/$', deletes.delete_ns, name='delete'),
        url(r'^dp/$', k8s.Dp_list.as_view(), name='test'),
        url(r'^dp/(?P<types>.*)$', k8s.Add_Mod_Dp.as_view(), name='test'),
        url(r'^select/(?P<types>.*)', k8s.SelectType.as_view(), name='ls_ns')
    ]))
]
