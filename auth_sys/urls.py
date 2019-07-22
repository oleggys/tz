from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='auth_sys/login_page.html'), name="login"),
    path('registration/', views.RegistrationView.as_view(), name="registration"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
]
