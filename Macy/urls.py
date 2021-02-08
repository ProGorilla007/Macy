from . import views
from django.urls import path

# シンプル、おしゃれ、ミニマリスティック、かわいいの要素。

urlpatterns = [
	path('signup/', views.SignupView.as_view(), name='signup'),
	path('login/', views.LogInView.as_view(), name="login"),
	path('about/', views.AboutView.as_view(), name='about'),
	path('guide/', views.GuideView.as_view(), name='guide'),
	path('contact/', views.ContactView.as_view(), name='contact'),
	path('account/<slug:slug>/', views.AccountView.as_view(), name='users'),
	path('account/<slug:slug>/delete/', views.UserDeleteView.as_view(), name='delete'),
	path('account/<slug:slug>/edit/', views.UserEditView.as_view(), name='edit'),
	path('account/<slug:slug>/password_change/', views.UserPasswordChangeView.as_view(), name='password_change'),
	path('account/<slug:slug>/password_change/done/', views.UserPasswordChangeDoneView.as_view(), name='password_change_done'),
	path('password_reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
	path('password_reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
	path('password_reset/confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('password_reset/complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
	path('<slug:slug>/', views.MypageView.as_view(), name='mypage'),
	path('', views.IndexView.as_view(), name='index'),
	]
