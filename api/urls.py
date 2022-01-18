from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('accounts/login/', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('accounts/password/reset/', views.ResetPassword.as_view(), name='reset-password'),
    path('accounts/password/reset/forget/', views.ForgetPassword.as_view(), name='reset-password-confirm'),
    path('accounts/password/reset/confirm/', views.LinkForgetPasswordReset.as_view(), name='reset-password-confirm'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('user/order/leads/', views.OrderLeadsView.as_view(), name='order-leads'),
    path('user/check/activation/', views.CheckUserActivationView.as_view(), name='chack-activation'),
    path('user/add/machine/', views.AddNewMachineView.as_view(), name='add-new-machine'),
    path('admin/users/subcription/', views.UsersSubscriptionView.as_view(), name='subscriptions'),
    path('admin/upload/leads/', views.AdminUploadLeadsView.as_view(), name='upload-leads'),
]