from user_management_app.models import *
from user_management_app.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from user_management_app.pagination import  StandardResultSetPagination
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from fcm_django.models import FCMDevice
from django.contrib.auth import authenticate
from rest_framework.generics import ListAPIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
from rest_framework.authentication import TokenAuthentication
from django.conf import settings
import stripe



class UserSignUpAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        
        if not username or not email or not password or not confirm_password:
            return Response({'success':False, 'response':{'message':'All fields are required!'}}, status=status.HTTP_400_BAD_REQUEST)
        
        if password != confirm_password:
            return Response({'success':False, 'response':{'message': 'password do mot match!'}}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).first():
            return Response({'success': False, 'response': {'message': 'Username already taken!'}}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).first():
            return Response({'success': False, 'response': {'message': 'Email already registered!'}}, status=status.HTTP_400_BAD_REQUEST)
  
        user = User.objects.create(username=username, email=email, password=password)
        user.set_password(password)
        user.is_active=True
        user.save()
        
        token, created = Token.objects.get_or_create(user=user)
        serializer = CreateUserSerializer(user)
        return Response({'success':True, 'response':{'data':serializer.data, 'access token':token.key}}, status=status.HTTP_200_OK)
    

class SocialLoginApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email').lower().strip() if 'email' in request.data else None
        user_d_id = request.data.get('device_id', None)
        full_name = request.data.get('full_name', None)
        social_platform = request.data.get('social_platform', None)

        if not email or not user_d_id or not social_platform:
            return Response({"success": False, 'response': {'message': 'email, device id, and social_platform required!'}},
                            status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(email=email).first()        
        if not user:
            username = email.split('@')[0]
            hashed_password = make_password(username)
            user = User.objects.create(
                username=username,
                password=hashed_password,
                email=email,
                full_name=full_name,
                social_platform=social_platform,
            )

        user.is_active = True
        user.save()

        token, created = Token.objects.get_or_create(user=user)

        access_token = token.key
        
        wallet, created = Wallet.objects.get_or_create(user=user)
        serializer = SocialLoginSerializer(user)
        
        try:
            fcm_device = FCMDevice.objects.get(device_id=user.id)
            fcm_device.delete()
        except:
            pass

        if user_d_id:
            fcm_device, created = FCMDevice.objects.get_or_create(
                registration_id=user_d_id,
                defaults={'user': user, 'device_id': user_d_id}
            )

        return Response({'success': True, 'response': {'data': serializer.data, 'access_token': access_token}}, status=status.HTTP_200_OK)



class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'success':False, 'response':{'message':'Username and password are required!'}}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'success':False, 'response':{'message':'Invalid username or password!'}}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_superuser and user.is_admin and user.user_type == 'user':
            user.user_type = 'admin'

        user.is_active = True
        user.save()

        token, created = Token.objects.get_or_create(user=user)
        serializer = CreateUserSerializer(user)
        return Response({'success':True, 'response':{'data':serializer.data, 'access token':token.key}}, status=status.HTTP_200_OK)
        
        
class UpdateProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        user = request.user        
        serializer = UpdateProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':True, 'response':{'data':serializer.data}}, status=status.HTTP_200_OK)
        


class CreateRepresentativeAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        username = request.data.get('username')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        # Validate required fields
        if not email or not phone_number or not username or not password or not confirm_password:
            return Response({'success': False, 'response': {'message': 'All fields are required!'}}, status=status.HTTP_400_BAD_REQUEST)

        if password != confirm_password:
            return Response({'success': False, 'response': {'message': 'Passwords do not match!'}}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'success': False, 'response': {'message': 'Email already registered!'}}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(phone_number=phone_number).exists():
            return Response({'success': False, 'response': {'message': 'Phone number already in use!'}}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'success': False, 'response': {'message': 'Username already taken!'}}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare data with defaults
        data = request.data.copy()
        data['full_name'] = username  # set full_name same as username

        serializer = RepresentativeSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            user.username = username
            user.set_password(password)
            user.is_active = True
            user.user_type = 'representative'
            user.save()

            token, created = Token.objects.get_or_create(user=user)
            return Response({'success': True, 'response': {'data': serializer.data, 'access token': token.key}}, status=status.HTTP_201_CREATED)

        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




class RepresentativeListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = RepresentativeSerializer
    pagination_class = StandardResultSetPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = []
    filterset_fields = []

    def get_queryset(self):
        rep_id = self.request.query_params.get('id', None)
        if rep_id:
            return User.objects.filter(id=rep_id, user_type='representative')
        return User.objects.filter(user_type='representative')




class SlotListAPIView(APIView):
    def get(self, request):
        duration = request.GET.get('duration')

        slots = Slot.objects.all()
        if duration:
            try:
                duration = int(duration)
                filtered_slots = []
                for slot in slots:
                    start = datetime.combine(datetime.today(), slot.start_time)
                    end = datetime.combine(datetime.today(), slot.end_time)
                    time_diff = (end - start).total_seconds() / 60

                    if int(time_diff) == duration:
                        filtered_slots.append(slot)

                slots = filtered_slots
            except ValueError:
                return Response({"error": "Invalid duration parameter"}, status=400)

        serializer = SlotSerializer(slots, many=True)
        return Response({'success':True, 'response':{'data': serializer.data}}, status=status.HTTP_200_OK)
    


class BookingAPIView(APIView):
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        service_price = data['service_price']
        slot = data['slot']
        booking_date = data['booking_date']


        # Create booking
        booking = Booking.objects.create(**data)

        # Calculate fees (5% GST + 3% Stripe)
        base_price = float(service_price.price)
        gst = round(base_price * 0.05, 2)
        stripe_fee = round(base_price * 0.03, 2)
        total = base_price + gst + stripe_fee

        # Prepare response
        response_data = {
            "booking": BookingSerializer(booking).data,
            "calculated_charges": {
                "base_price": base_price,
                "gst_5%": gst,
                "stripe_fee_3%": stripe_fee,
                "total_amount": total
            },
            "slot_info": str(slot),
            "representative": {
                "id": booking.representative.id,
                "name": booking.representative.get_username()
            }
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    



class RepresentativeNotes(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    serializer_class = RepresentativeNotesSerializer
    pagination_class = StandardResultSetPagination

    def get_queryset(self):
        rep_id = self.request.query_params.get('id', None)
        if rep_id:
            return User.objects.filter(id=rep_id, user_type='representative')
        return User.objects.filter(user_type='representative')

    def patch(self, request, id):
        rep_qs = User.objects.filter(id=id, user_type='representative')
        if not rep_qs.exists():
            return Response({"detail": "Representative not found."}, status=status.HTTP_404_NOT_FOUND)

        rep = rep_qs.first()
        serializer = RepresentativeNotesSerializer(rep, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        rep_qs = User.objects.filter(id=id, user_type='representative')
        if not rep_qs.exists():
            return Response({"detail": "Representative not found."}, status=status.HTTP_404_NOT_FOUND)

        rep = rep_qs.first()
        rep.rep_note = None  # or "" if it's a CharField
        rep.save()

        return Response({"detail": "Representative note removed."}, status=status.HTTP_200_OK)


class TotalUsers(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        total_users = User.objects.filter(user_type='user' ,is_active=True).count()
        total_representatives = User.objects.filter(user_type='representative', is_active=True).count()
        total_admins = User.objects.filter(user_type='admin', is_active=True).count()
        
        return Response({
            'success': True,
            'response': {
                'total_users': total_users,
                'total_representatives': total_representatives,
                'total_admins': total_admins
            }
        }, status=status.HTTP_200_OK)
        
class BlockUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        user_to_block = User.objects.filter(id=id).first()
        if not user_to_block:
            return Response({'success': False, 'response': {'message': 'User not found!'}}, status=status.HTTP_404_NOT_FOUND)

        user_to_block.is_active = False
        user_to_block.save()

        return Response({'success': True, 'response': {'message': 'User Blocked successfully!'}}, status=status.HTTP_200_OK)
    
    
class DeleteUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        user_to_delete = User.objects.filter(id=id, user_type='user').first()

        if not user_to_delete:
            return Response({'success': False, 'message': 'User not found or not of type "user".'}, status=status.HTTP_404_NOT_FOUND)

        user_to_delete.delete()

        return Response({'success': True, 'message': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class BlockedUserListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateUserSerializer
    pagination_class = StandardResultSetPagination

    def get_queryset(self):
        return User.objects.filter(is_active=False, user_type='user')

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['username', 'email']
    filterset_fields = ['username', 'email']
    
    
    
from google.oauth2 import service_account
from googleapiclient.discovery import build
import uuid

def create_google_meet_event(start_time, end_time, summary="Scheduled Meeting"):
    SERVICE_ACCOUNT_FILE = 'creds/true-feelings-461303-a0cf3ed970a9.json'  # Example: 'google/credentials.json'
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    service = build('calendar', 'v3', credentials=credentials)

    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time,
            'timeZone': 'Asia/Karachi',  # Adjust to your preferred timezone
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Asia/Karachi',
        },
        'conferenceData': {
            'createRequest': {
                'requestId': str(uuid.uuid4()),
                'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            }
        }
    }

    created_event = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1
    ).execute()

    return created_event.get('hangoutLink')


class ScheduleMeetingView(APIView):
    def post(self, request):
        try:
            start_time = request.data.get('start_time')  # ISO format: '2025-05-30T12:00:00'
            end_time = request.data.get('end_time')      # ISO format: '2025-05-30T13:00:00'
            summary = request.data.get('summary', 'Online Meeting')

            meet_link = create_google_meet_event(start_time, end_time, summary)

            return Response({'meet_link': meet_link}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)




class CreatePaymentIntentAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        amount = request.data.get('amount')

        if not amount:
            return Response({"success": False, "message": "Amount is required."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            amount = int(float(amount) * 100)  # amount in cents
        except ValueError:
            return Response({"success": False, "message": "Invalid amount."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                payment_method_types=['card'],
            )
            return Response({"success": True, "client_secret": intent.client_secret},
                            status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
            return Response({"success": False, "message": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class PaymentAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CheckPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        client_secret = serializer.validated_data['client_secret']

        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY

            # Extract the PaymentIntent ID from client_secret
            payment_intent_id = client_secret.split('_secret')[0]

            intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            if intent.status == 'succeeded':
                return Response({"success": True, "response": {"message": "Payment Successful"}},
                                status=status.HTTP_200_OK)
            else:
                return Response({"success": False, "response": {"message": "Payment Incomplete"}},
                                status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.StripeError as e:
            return Response({"success": False, "response": {"message": str(e)}},
                            status=status.HTTP_400_BAD_REQUEST)




# hbrsdkjgkjdjnf