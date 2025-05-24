from django.contrib import admin
from .models import Technician, ServiceRequest, Appointment, Payment, CustomerProfile

# Register your models here.
@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'specialization', 'experience_years', 'is_available')
    list_filter = ('specialization', 'is_available')
    search_fields = ('user__username', 'user__email', 'specialization')

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'device_type', 'status', 'created_at', 'technician')
    list_filter = ('status', 'device_type', 'created_at')
    search_fields = ('customer__username', 'device_type', 'issue_description')
    date_hierarchy = 'created_at'

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_request', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('status', 'appointment_date')
    search_fields = ('service_request__device_type', 'notes')
    date_hierarchy = 'appointment_date'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_request', 'amount', 'payment_method', 'status', 'payment_date')
    list_filter = ('status', 'payment_method', 'payment_date')
    search_fields = ('service_request__device_type', 'transaction_id')
    date_hierarchy = 'payment_date'

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone_number', 'preferred_contact_method')
    list_filter = ('preferred_contact_method',)
    search_fields = ('user__username', 'user__email', 'phone_number')
