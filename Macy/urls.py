from . import views
from django.urls import path, include

urlpatterns = [
	path('signup/', views.SignupView.as_view(), name='signup'),
	path('login/', views.LogInView.as_view(), name="login"),
	path('about/', views.AboutView.as_view(), name='about'),
	path('guide/', views.GuideView.as_view(), name='guide'),
	path('contact/', views.ContactView.as_view(), name='contact'),
	path('<slug:slug>/', views.MypageView.as_view(), name='mypage'),
	path('account/<slug:slug>/', views.AccountView.as_view(), name='users'),
	path('account/<slug:slug>/delete/', views.UserDelete.as_view(), name='delete'),
	path('account/<slug:slug>/edit/', views.UserEditView.as_view(), name='edit'),
	path('password_change/<int:pk>', views.PasswordChange.as_view(), name='password_change'),
	path('password_change/done/<int:pk>', views.PasswordChangeDone.as_view(), name='password_change_done'),
	path('', views.IndexView.as_view(), name='index'),
	]

