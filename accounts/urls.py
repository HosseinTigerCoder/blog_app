from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register_user,name='register'),
    path('profile/',views.profile_page,name='profile'),
    path('password-reset',views.password_reset,name='password_reset'),
    path('reset/<uidb64>/<token>/',views.set_new_password,name='set_new_password'),
    path('contact-us/',views.contact_us,name='contact_us'),
    path('tickets/',views.ticket_list,name='tickets'),
    path('create-ticket/',views.create_ticket,name='create_ticket'),
    path('tickets/<int:pk>',views.reply_ticket,name='ticket_detail')
]
  