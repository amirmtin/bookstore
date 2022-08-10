from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    # registration
    path(
        route='signup/', 
        view=views.UserSignUpView.as_view(), 
        name='signup'
    ),
    path(
        route='active/<uidb64>/<token>/', 
        view=views.VerifyEmailView.as_view(), 
        name='verify'
    ),
    path(
        route='send_email/', 
        view=views.ActiveEmailView.as_view(), 
        name='send_email'
    ),
    path(
        route='login/', 
        view=views.UserLoginView.as_view(), 
        name='login'
    ),
    path(
        route='logout/', 
        view=views.UserLogoutView.as_view(), 
        name='logout'
    ),
    # profile
    path(
        route='dashboard/', 
        view=views.UserDashboardView.as_view(), 
        name='dashboard'
    ),
    # reset password
    path(
        route='reset/', 
        view=views.PasswordResetView.as_view(), 
        name='reset'
    ),
    path(
        route='reset_done/', 
        view=views.PasswordResetDoneView.as_view(), 
        name='reset_done'
    ),
    path(
        route='reset_confirm/<uidb64>/<token>/', 
        view=views.PasswordResetConfirmView.as_view(), 
        name='reset_confirm'
    ),
    path(
        route='reset_complete/', 
        view=views.PasswordResetCompleteView.as_view(), 
        name='reset_complete'
    ),
]
