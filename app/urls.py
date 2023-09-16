from django.urls import path
from .views import (RegisterView,
                    LoginView,
                     UpdateProfileDetails,
                      AdminPanel,
                      # CustomUserListView,
                      LogoutView,
                    )
from rest_framework_simplejwt.tokens import BlacklistedToken

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register-view"),
    path("login/", LoginView.as_view(), name="login-view"),
    path('update/', UpdateProfileDetails.as_view(), name="update-profile"),   
    path('list/<int:pk>/', AdminPanel.as_view(), name="profile"),   
    path('list/', AdminPanel.as_view(), name="profile"),   
    path('logout/', LogoutView.as_view(), name='logout-user'),   
    # path('userlist/', CustomUserListView.as_view(), name="=list-profile"),
    
]
