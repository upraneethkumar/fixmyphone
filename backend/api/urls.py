from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'service-requests', views.ServiceRequestViewSet, basename='service-request')
router.register(r'appointments', views.AppointmentViewSet, basename='appointment')
router.register(r'payments', views.PaymentViewSet, basename='payment')
router.register(r'technicians', views.TechnicianViewSet, basename='technician')
router.register(r'customer-profiles', views.CustomerProfileViewSet, basename='customer-profile')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('admin-dashboard/', views.admin_dashboard_data, name='admin-dashboard'),
    path('user-dashboard/', views.user_dashboard_data, name='user-dashboard'),
]
