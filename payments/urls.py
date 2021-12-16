from django.urls import path
from . import views


app_name = 'payments'
urlpatterns = [
    path('', views.PaymentListAPIView.as_view(), name='payment_list'),
    path('add/', views.PaymentCreateAPIView.as_view(), name='payment_create'),
    path('<ref>/', views.PaymentDetailView.as_view(), name='payment_detail'),
]
