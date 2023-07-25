from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime
from django.core.mail import send_mail
from django.urls import reverse
from .utils import generate_token
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.
class RegisterView(APIView):
    def post(self,req):
        print(req.data)
        serializers = UserSerializer(data = req.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        user = User.objects.filter(email=req.data['email']).first()
        token = generate_token.make_token(user)
        domain = get_current_site(req).domain
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        link = reverse('activate',kwargs={
            'uidb64': uidb64,
            'token': token,
        })
        activationURL = 'http://'+domain+link
        subject = 'MakeAI activation email'
        message = f'Hi {user.name},\n\n\nThank you for registering with MakeAI.\nKindly activate your account by clicking on the following link\n '+activationURL
        email_from = 'dev.makeai@gmail.com'
        recipient_list = [user.email, ]
        send_mail( subject, message, email_from, recipient_list )
        return Response(serializers.data)

class LoginView(APIView):
    def post(self,req):
        email = req.data['email']
        password = req.data['password']

        user = User.objects.filter(email=email).first()
        print(user.pk)
        if user is None:
            raise AuthenticationFailed("No such user exists")
        if not user.is_active:
            raise AuthenticationFailed("Please Activate you account. Link has been sent to registered email ID.") 
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password") 

        payload = {
            'id':user.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=2),
            'iat' : datetime.datetime.utcnow(),
        }
        token = jwt.encode(payload,'secret',algorithm='HS256')#.decode('utf8')
        res = Response()
        res.set_cookie(key='jwt',value=token,httponly=True)
        res.data =  {
            'jwt':token,
        }
        return res

class UserView(APIView):
    def get(self,req):
        token = req.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unautharized :(")
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
        print(token,payload)
        try:
            payload = jwt.decode(token,'secret',algorithms='HS256')
        except:
            raise AuthenticationFailed("signature expired Login in Agaiin!!")
        
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

class ActivateView(APIView):
    def get(self,req,uidb64,token):

        uidb64 = urlsafe_base64_decode(uidb64)
        print(int(uidb64))
        user = User.objects.filter(id=uidb64).first()
        user.is_active = True
        user.save()
        return Response({'message':'account activated'})

class RequestResetPasswordView(APIView):
    def post(self,req):
        user = User.objects.filter(email=req.data['email']).first()
        token = generate_token.make_token(user)
        domain = get_current_site(req).domain
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        link = reverse('reset',kwargs={
            'uidb64': uidb64,
            'token': token,
        })
        activationURL = 'http://'+domain+link
        subject = 'MakeAI account password reset email'
        message = f'Hi {user.name},\n\n\nPlease use the following link to reset your MakeAI account.\n '+activationURL
        email_from = 'dev.makeai@gmail.com'
        recipient_list = [user.email, ]
        send_mail( subject, message, email_from, recipient_list )
        return Response({'message':'Password reset email sent. Please check your inbox'})

class ResetPasswordView(APIView):
    def post(self,req,uidb64,token):
        uidb64 = urlsafe_base64_decode(uidb64)
        print(int(uidb64))
        user = User.objects.filter(id=uidb64).first()
        user.set_password(req.data['NewPassword'])
        user.save()
        return Response({'message':'Password reset'})

class LogoutView(APIView):
    def post(self,req):
        res = Response()
        res.delete_cookie('jwt')
        res.data = {
            'message':'success',
        }
        return res


class ClearDatabaseView(APIView):
    def post(self,req):
        User.objects.all().delete()
        return Response({
            'message': 'deleted entire database',
        })