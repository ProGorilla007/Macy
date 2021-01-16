from django.urls import path
from . import views

urlpatterns = [
	path('signup/', views.SignupView.as_view(), name='signup'),
	path('account_info/', views.AccountView.as_view(), name='account'),
	path('user_list/', views.UserList.as_view(), name='user_list'),
	path('', views.IndexView.as_view(), name='index_view'),
]
