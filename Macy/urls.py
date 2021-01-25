from . import views
from django.urls import path, include
from django.contrib.auth.decorators import login_required

urlpatterns = [
	path('signup/', views.SignupView.as_view(), name='signup'),
	# path('account/<name>', views.AccountView.as_view(), name='account'),
	path('user_list/', views.UserList.as_view(), name='user_list'),
	path('login/', views.LogInView.as_view(), name="login_view"),
	path('delete/<int:pk>', views.UserDelete.as_view(), name='delete'),
	path('', views.IndexView.as_view(), name='index_view'),
	# path('admin/', admin.site.urls),
	# djangoがデフォルトで用意している機能の追加（ログイン、ログアウト、パスワード変更、パスワード再発行）
	# path("", login_required(index_view), name="index"),
	path('', include("django.contrib.auth.urls")),
]
