from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserCreate.as_view(), name='account-create'),
    path('user-lookup-email/', views.UserExistsByEmail.as_view(), name='user-lookup-email'),
]