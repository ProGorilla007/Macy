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
	path('reset_password/<int:pk>', auth_views.PasswordResetView.as_view(), name='reset_password'),
	path('reset_password_sent/<int:pk>', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('reset_password_complete/<int:pk>', auth_views.PasswordResetCompleteView .as_view(), name='password_reset_complete'),
	path('', views.IndexView.as_view(), name='index'),
	]

