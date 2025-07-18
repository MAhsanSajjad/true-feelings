from django.urls import path
from user_management_app.views import *
from . import views

urlpatterns = [
    path('Signup/', UserSignUpAPIView.as_view()),
    path('SocialLogin/', SocialLoginApiView.as_view()),
    path('Login/', LoginAPIView.as_view()),
    path('UpdateProfile/', UpdateProfileAPIView.as_view()),
    path('CreateRepresentative/', CreateRepresentativeAPIView.as_view()),
    path('RepresentativeList/', RepresentativeListAPIView.as_view()),
    path('RepresentativeList/<int:id>/', RepresentativeListAPIView.as_view()),
    path('SlotList/', SlotListAPIView.as_view()),
    path('Booking/', BookingAPIView.as_view()),
    path('RepresentativeNotes/', views.RepresentativeNotes.as_view()),
    path('RepresentativeNotes/<int:id>/', views.RepresentativeNotes.as_view()),
    path('TotalUserCount/', views.TotalUsers.as_view()),
    path('BlockUser/<int:id>/', views.BlockUserAPIView.as_view()),
    path('DeleteUser/<int:id>/', views.DeleteUserAPIView.as_view()),
    path('BlockedUserList/', views.BlockedUserListAPIView.as_view()),
    path('schedule-meeting/', ScheduleMeetingView.as_view(), name='schedule-meeting'),
    path('BookingPayment/', views.PaymentAPIView.as_view()),
    path('createclientid/', views.CreatePaymentIntentAPIView.as_view())

    


]
