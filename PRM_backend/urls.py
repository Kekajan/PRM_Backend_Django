from django.contrib import admin
from django.urls import path, re_path
from prm import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^user$', views.signup),
    re_path(r'^user/([0-9]+)$', views.signup),
    re_path(r'^login_user$', views.login_user),
    re_path(r'^project$', views.projectApi),
    re_path(r'^project/([0-9]+)$', views.projectApi),
    re_path(r'^task$', views.taskApi),
    re_path(r'^task/([0-9]+)$', views.taskApi)
]
