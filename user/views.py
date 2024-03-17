from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserSerializer,LogInUserSerializer
from django.core.mail import send_mail
import random
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework import viewsets,generics
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

@extend_schema(responses=LogInUserSerializer) 
class LoginApiView(generics.GenericAPIView):
    serializer_class=LogInUserSerializer
    def post(self,request, format=None):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
         
        return  Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token":AuthToken.objects.create(user)[1]
        })
         

class UsersApiView(generics.ListAPIView):
    queryset =CustomUser.objects.all()
    serializer_class=UserSerializer

class RegistrationView(APIView):
    def post(self,request):
        email = request.data.get('email')
        image_profile= request.data.get('image_profile')
        first_name= request.data.get('first_name')
        last_name= request.data.get('last_name')


        phone_number=request.data.get('phone_number')
        national_code=request.data.get('national_code')

        password=request.data.get('password')





        code = str(random.randint(100000, 999999))
        user = CustomUser(email=email, code=code,image_profile=image_profile,first_name=first_name,last_name=last_name,phone_number=phone_number,national_code=national_code,password=password)
        user.is_active =False
        user.save()
        print("code",code)
        # Send the verification code to the user's email
        send_mail(
            'کد ثبت نام',
            f'کد ثبت نام شما :{code}',
            'azizzadepouya8@gmail.com',
            [email],
            fail_silently=False,
        )
        
        serializer = UserSerializer(user)
        return Response(serializer.data)
class VerifyCodeView(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        
        try:
            user = CustomUser.objects.get(email=email, code=code)
        except CustomUser.DoesNotExist:
            return Response({'error': 'کد اشتباه است'}, status=400)
        
        user.is_active= True
        user.save()
        
        serializer = UserSerializer(user)
        return Response({
            "user": serializer.data,
            "token": AuthToken.objects.create(user)[1]
        })
    
