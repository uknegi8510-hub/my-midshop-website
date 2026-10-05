from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from Accounts.serializer import UserSerializer,VerifyRegisterSerializer,LoginSerializer,VerifyLoginSerializer
from .emails import *
from django.contrib.auth import login,logout
from django.utils import timezone



def login_page(request):
    return render(request,'login_page.html')


def logout_page(request):
    logout(request)
    return render(request,'index.html')


class RegisterAPI(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                send_register_otp(serializer.data['email'])
                return Response({
                    'status': 200,
                    'message': "registration successful, check email",
                    'data': serializer.data,
                })

            return Response({
                'status': 400,
                'message': "Something went wrong",
                'data': serializer.errors,
            })

        except Exception as e:
            return Response({
                'status':500,
                'message':str(e)
            })


class VerifyRegisterOTP(APIView):
    authentication_classes=[]
    permission_classes=[AllowAny]
    def post(self,request):
        try:
            data=request.data
            serializer=VerifyRegisterSerializer(data=data)
            if serializer.is_valid():
                email=serializer.data['email']
                register_otp=serializer.data['register_otp']
                user=User.objects.filter(email=email)


                if not user.exists():
                    return Response({
                        'status':400,
                        'message':"something went wrong",
                        'data':'invalid emial',
                    })
                user=user.first()
                if not user.register_otp==register_otp:
                    return Response({
                        'status':400,
                        'message':"something went wrong",
                        'data':'wrong otp',
                    })
                
                user.is_verified=True
                user.save()
                login(request,user)
                return Response({
                    'status':200,
                    'message':"account  verified",
                    'data':serializer.data
                })
            pass
        except Exception as e:
            print(e)
            
class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            email = user.email

            # Send OTP
            send_login_otp(email)

            return Response({
                "status": 200,
                "message": "OTP sent to email"
            })

        return Response({
            "status": 400,
            "errors": serializer.errors
        })
            
class VerifyLoginOTP(APIView):
    authentication_classes = []   # 👈 disable session auth
    permission_classes = [AllowAny]

    def post(self,request):
        try:
            data=request.data
            serializer=VerifyLoginSerializer(data=data)
            if serializer.is_valid():
                email=serializer.validated_data['email']
                login_otp=serializer.validated_data['login_otp']
                user=User.objects.filter(email=email)
                if not user.exists():
                    return Response({
                        "status":400,
                        "message":"User not exists",
                        "data":"Invalid email"
                    })
                user=user.first()
                if user.login_otp!=login_otp:
                    return Response({
                        "status":400,
                        "message":"something went wrong",
                        "data":"wrong OTP"
                    })
                user.login_otp = None
                user.last_login_time=timezone.now()
                user.save()
                login(request,user)
                return Response({
                    'status':200,
                    "message":"Account Verified",
                    'data':serializer.data
                })
        except Exception as e:
            print(e)
            return Response({
                "status": 500,
                "message": "Server error"
            })
