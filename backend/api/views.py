from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authtoken.models import Token

from .models import Technician, ServiceRequest, Appointment, Payment, CustomerProfile
from .serializers import (
    UserSerializer, TechnicianSerializer, ServiceRequestSerializer,
    AppointmentSerializer, PaymentSerializer, CustomerProfileSerializer,
    UserRegistrationSerializer
)

# User Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

# Login View
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user:
        # Check if user is a technician or admin
        is_technician = hasattr(user, 'technician_profile')
        is_admin = user.is_staff

        return Response({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_technician': is_technician,
            'is_admin': is_admin,
        })
    else:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

# Service Request ViewSet
class ServiceRequestViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # If user is admin or technician, show all requests
        if user.is_staff or hasattr(user, 'technician_profile'):
            return ServiceRequest.objects.all()

        # Otherwise, show only user's requests
        return ServiceRequest.objects.filter(customer=user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

# Appointment ViewSet
class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # If user is admin or technician, show all appointments
        if user.is_staff or hasattr(user, 'technician_profile'):
            return Appointment.objects.all()

        # Otherwise, show only user's appointments
        return Appointment.objects.filter(service_request__customer=user)

# Payment ViewSet
class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # If user is admin, show all payments
        if user.is_staff:
            return Payment.objects.all()

        # Otherwise, show only user's payments
        return Payment.objects.filter(service_request__customer=user)

# Technician ViewSet (Admin only for creation/update/delete)
class TechnicianViewSet(viewsets.ModelViewSet):
    queryset = Technician.objects.all()
    serializer_class = TechnicianSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

# Customer Profile ViewSet
class CustomerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # If user is admin, show all profiles
        if user.is_staff:
            return CustomerProfile.objects.all()

        # Otherwise, show only user's profile
        return CustomerProfile.objects.filter(user=user)

# Dashboard Data View for Admin
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_dashboard_data(request):
    total_requests = ServiceRequest.objects.count()
    pending_requests = ServiceRequest.objects.filter(status='pending').count()
    in_progress_requests = ServiceRequest.objects.filter(status='in_progress').count()
    completed_requests = ServiceRequest.objects.filter(status='completed').count()

    total_technicians = Technician.objects.count()
    available_technicians = Technician.objects.filter(is_available=True).count()

    total_customers = CustomerProfile.objects.count()

    upcoming_appointments = Appointment.objects.filter(
        status='confirmed'
    ).count()

    return Response({
        'service_requests': {
            'total': total_requests,
            'pending': pending_requests,
            'in_progress': in_progress_requests,
            'completed': completed_requests,
        },
        'technicians': {
            'total': total_technicians,
            'available': available_technicians,
        },
        'customers': {
            'total': total_customers,
        },
        'appointments': {
            'upcoming': upcoming_appointments,
        }
    })

# Dashboard Data View for User
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard_data(request):
    user = request.user

    user_requests = ServiceRequest.objects.filter(customer=user)
    total_requests = user_requests.count()
    pending_requests = user_requests.filter(status='pending').count()
    in_progress_requests = user_requests.filter(status='in_progress').count()
    completed_requests = user_requests.filter(status='completed').count()

    upcoming_appointments = Appointment.objects.filter(
        service_request__customer=user,
        status='confirmed'
    ).count()

    return Response({
        'service_requests': {
            'total': total_requests,
            'pending': pending_requests,
            'in_progress': in_progress_requests,
            'completed': completed_requests,
        },
        'appointments': {
            'upcoming': upcoming_appointments,
        }
    })
