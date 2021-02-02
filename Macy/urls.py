from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views

# シンプル、おしゃれ、ミニマリスティック、かわいいの要素。

urlpatterns = [
	path('signup/', views.SignupView.as_view(), name='signup'),
	path('login/', views.LogInView.as_view(), name="login"),
	path('about/', views.AboutView.as_view(), name='about'),
	path('guide/', views.GuideView.as_view(), name='guide'),
	path('contact/', views.ContactView.as_view(), name='contact'),
	path('<int:pk>/', views.AccountView.as_view(), name='users'),
	path('delete/<int:pk>', views.UserDelete.as_view(), name='delete'),
	path('password_change/<int:pk>', views.PasswordChange.as_view(), name='password_change'),
	path('password_change/done/<int:pk>', views.PasswordChangeDone.as_view(), name='password_change_done'),
	path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
	path('password_reset/done/<int:pk>', views.PasswordResetDone.as_view(), name='password_reset_done'),
	path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
	path('password_reset/complete/<int:pk>', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
	path('', views.IndexView.as_view(), name='index'),
	]

