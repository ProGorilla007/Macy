from . import views
from django.urls import path, include
from django.contrib.auth.decorators import login_required

urlpatterns = [
	path('signup/', views.SignupView.as_view(), name='signup'),
	# path('account/<name>', views.AccountView.as_view(), name='account'),
	path('user_list/', views.UserList.as_view(), name='user_list'),
	path('login/', views.LogInView.as_view(), name="login_view"),
	path('', views.IndexView.as_view(), name='index_view'),
]
