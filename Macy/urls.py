from . import views
from django.urls import path, include
from django.contrib.auth.decorators import login_required

urlpatterns = [
	path('signup/', views.SignupView.as_view(), name='signup'),
	path('login/', views.LogInView.as_view(), name="login"),
	path('about/', views.AboutView.as_view(), name='about'),
	path('guide/', views.GuideView.as_view(), name='guide'),
	path('contact/', views.ContactView.as_view(), name='contact'),
	path('<int:pk>/', views.AccountView.as_view(), name='users'),
	path('', views.IndexView.as_view(), name='index'),
]
