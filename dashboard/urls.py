from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from . import views 

urlpatterns = [
    path('', views.Adminloginview.as_view(),name='admin-login'),
    path('index/', IndexView.as_view(), name='index'),
    path('admin-logout/',Adminlogout.as_view(),name='admin_logout'),
    path('admin-profile/', AdminUpdateProfile.as_view(), name='admin-profile'),

    path('admin-changepassord/',Admin_changepassord.as_view(),name='admin_changepassord'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('customer-list/',CustomerList.as_view(),name='customer_list'),
    path('add-customer/',AddCustomer.as_view(),name='add_customer'),
    path('edit-customer/<int:id>',EditCustomer.as_view(),name='edit_customer'),
    path('delete-customer/<int:id>/',DeleteCustomer.as_view(),name='delete_customer'),
    path('customer-active-inactive/<int:id>/', CustomerActiveinactive.as_view(), name='customer-active-inactive'),



]