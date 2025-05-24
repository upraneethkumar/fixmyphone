from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Technician, ServiceRequest, Appointment, Payment, CustomerProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class TechnicianSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Technician
        fields = ['id', 'user', 'specialization', 'experience_years', 'is_available']
        read_only_fields = ['id']

class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = CustomerProfile
        fields = ['id', 'user', 'phone_number', 'address', 'preferred_contact_method']
        read_only_fields = ['id']

class ServiceRequestSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    technician_name = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceRequest
        fields = [
            'id', 'customer', 'customer_name', 'technician', 'technician_name',
            'device_type', 'issue_description', 'status', 'created_at',
            'updated_at', 'estimated_completion'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_customer_name(self, obj):
        return obj.customer.get_full_name() if obj.customer else None
    
    def get_technician_name(self, obj):
        return obj.technician.user.get_full_name() if obj.technician else None

class AppointmentSerializer(serializers.ModelSerializer):
    service_request_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'service_request', 'service_request_details',
            'appointment_date', 'appointment_time', 'status', 'notes'
        ]
        read_only_fields = ['id']
    
    def get_service_request_details(self, obj):
        return {
            'id': obj.service_request.id,
            'device_type': obj.service_request.device_type,
            'issue': obj.service_request.issue_description[:50] + '...' if len(obj.service_request.issue_description) > 50 else obj.service_request.issue_description,
            'status': obj.service_request.status
        }

class PaymentSerializer(serializers.ModelSerializer):
    service_request_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Payment
        fields = [
            'id', 'service_request', 'service_request_details', 'amount',
            'payment_date', 'payment_method', 'status', 'transaction_id'
        ]
        read_only_fields = ['id', 'payment_date']
    
    def get_service_request_details(self, obj):
        return {
            'id': obj.service_request.id,
            'device_type': obj.service_request.device_type,
            'customer': obj.service_request.customer.get_full_name()
        }

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    phone_number = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'phone_number']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return data
    
    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number')
        password_confirm = validated_data.pop('password_confirm')
        
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        
        # Create customer profile
        CustomerProfile.objects.create(user=user, phone_number=phone_number)
        
        return user
