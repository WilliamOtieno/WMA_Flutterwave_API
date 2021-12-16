from django.urls import path
from . import views


app_name = 'users'
urlpatterns = [
    path('', views.UserListAPIView.as_view(), name='user_list'),
    path('<id>/', views.UserDetailAPIView.as_view(), name='user_detail')
]
