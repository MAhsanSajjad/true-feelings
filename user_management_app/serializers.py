from rest_framework import serializers
from .models import *

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type']
        
class SocialLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'social_platform']
        
        
class TransactionHistroySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistroy
        fields = ['id', 'wallet', 'amount', 'transaction_type']

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'age', 'gender', 'phone_number', 'whatsapp_no', 'email', 'city', 'province', 'logo']
        


class RepresentativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'full_name', 'email', 'phone_number', 'age', 'gender', 'city', 'province',
            'joining_date', 'designation', 'fixed_salary', 'per_call_price', 'services',
            'document', 'logo', 'user_type', 'salary_type'
        ]

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ['id', 'start_time', 'end_time']



class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'service', 'service_price', 'slot', 'booking_date', 'status', 'representative']
        
        
        
class RepresentativeNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'rep_note']
        
        
class CheckPaymentSerializer(serializers.Serializer):
    client_secret = serializers.CharField(max_length=255)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
