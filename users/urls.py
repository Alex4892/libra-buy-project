from django.urls import path

from .views import (login_view, logout_view,
                    register_user_view, view_profile, view_admin_dashboard)

app_name = "users"

urlpatterns = [
    path('registration/', register_user_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', view_profile, name='profile'),
    path('admin_dashboard/', view_admin_dashboard, name='admin_dashboard')
]
