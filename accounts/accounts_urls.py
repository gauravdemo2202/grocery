from django.urls import path
from django.contrib.auth import views as auth_views
import accounts.views as view


urlpatterns = [
    path(
        'login', 
        auth_views.LoginView.as_view(template_name='accounts/login.html'), 
        name='login'
        ),
    path(
        'logout', 
        auth_views.LogoutView.as_view(template_name='accounts/logout.html'), 
        name='logout'
        ),
    path('register', view.register, name='register'),
    path('my_account', view.my_account, name='my_account'),
    ]
