from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class RegisterView(APIView):
    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        if not all([name, email, password]):
            return Response({'error': 'name, email and password are required'}, status=400)

        if User.objects.filter(username=email).exists():
            return Response({'error': 'User already exists'}, status=400)

        try:
            # Username is set as the email
            user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'id': user.id,
                'email': user.email,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not all([email, password]):
            return Response({'error': 'email and password are required'}, status=400)

        user = authenticate(username=email, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=401)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'access_token': token.key,
            'user': {'id': user.id, 'email': user.email},
        }, status=status.HTTP_200_OK)
