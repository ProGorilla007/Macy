from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView

index_view = TemplateView.as_view(template_name="registration/index.html")

urlpatterns = [
	path('signup/', views.SignupView.as_view(), name='signup'),
	path('account_info/', views.AccountView.as_view(), name='account'),
	path('user_list/', views.UserList.as_view(), name='user_list'),
	path('', views.IndexView.as_view(), name='index_view'),
	path('admin/', admin.site.urls),
	#djangoがデフォルトで用意している機能を追加。
    path("", login_required(index_view), name="index"),
    path('', include("django.contrib.auth.urls")),
]
