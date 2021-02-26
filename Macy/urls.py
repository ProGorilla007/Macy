from . import views
from django.urls import path


# シンプル、おしゃれ、ミニマリスティック、かわいいの要素。

urlpatterns = [
	path('about/', views.AboutView.as_view(), name='about'),
	path('guide/', views.GuideView.as_view(), name='guide'),
	path('contact/', views.ContactView.as_view(), name='contact'),
	path('login/', views.LogInView.as_view(), name="login"),
	path('<uuid:id>/logout/', views.LogOutView.as_view(), name="logout"),
	path('<uuid:id>/signup/', views.SignupView.as_view(), name='signup'),
	path('<uuid:id>/account/', views.AccountView.as_view(), name='users'),
	path('<uuid:id>/account/edit/', views.UserEditView.as_view(), name='edit'),
	path('<uuid:id>/account/delete/', views.UserDeleteView.as_view(), name='delete'),
	path('<uuid:id>/account/delete/profile', views.DeleteProfileView.as_view(), name='delete_profile'),
	path('<uuid:id>/account/delete/header', views.DeleteHeaderView.as_view(), name='delete_header'),
	path('<uuid:id>/account/password_change/', views.UserPasswordChangeView.as_view(), name='password_change'),
	path('<uuid:id>/account/password_change/done/', views.UserPasswordChangeDoneView.as_view(), name='password_change_done'),
	path('<uuid:id>/account/direct/', views.IsDirectView.as_view(), name='is_direct'),
	path('<uuid:id>/', views.MypageView.as_view(), name='mypage'),
	path('password_reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
	path('password_reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
	path('password_reset/confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('password_reset/complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
	path('', views.IndexView.as_view(), name='index'),
	]
# log out 追加
