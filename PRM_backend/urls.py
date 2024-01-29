from django.contrib import admin
from django.urls import path, re_path

from prm import views
from prm import navaViews
from prm import userview

from prm import views, authViews


urlpatterns = [
    path('admin/', admin.site.urls),   
    re_path(r'^register$', authViews.RegisterApi),
    re_path(r'^login$', authViews.LoginApi),
    re_path(r'^project$', views.projectApi),
    re_path(r'^project/([0-9]+)$', views.projectApi),
    re_path(r'^task$', views.taskApi),
    re_path(r'^task/([0-9]+)$', views.taskApi),
    re_path(r'^username$', views.usernameApi),

    re_path(r'^user$', views.usernameApi),
    re_path(r'^setting$', navaViews.settingApi),
    re_path(r'^setting/([0-9]+)$', navaViews.settingApi),
    re_path(r'^settingPassword$', navaViews.settingasswordApi),
    re_path(r'^settingPassword/([0-9]+)$', navaViews.settingasswordApi),


    re_path(r'^taskproject/([0-9]+)$', views.taskProjectApi),

]
