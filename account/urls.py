from django.urls import path
from .views import register_user,CreateUserView,LoginView,select_role_view,citizen_dashboard,officer_dashboard,OTP_verification,chat_view,profile_view,logout_user

urlpatterns = [
    path("", select_role_view, name="select_role"),
    path("register/", register_user, name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),

    path("otp_verification/", OTP_verification.as_view(), name="otp_verification"),

    # path("citizen/lost/", lost_view, name="register"),
    # path("citizen/found/", found_view, name="register"),
    path("citizen/chat/", chat_view, name="register"),
    path("citizen/profile/", profile_view, name="register"),


    path("citizen_dashboard/", citizen_dashboard, name="citizen_dashboard"),
    path("officer_dashboard/", officer_dashboard, name="officer_dashboard"),


    path("createuser/", CreateUserView.as_view(), name="createuser"),

]