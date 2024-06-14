from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from .models import MyUser as User
from .serializers import UserSerializer, LoginSerializer
# Create your views here.

@api_view(['POST'])
def login(request: Request) -> Response:
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = request.data.get('email')

        # Check user exists
        user = User.objects.get(email=email)
                
        if not user:
            return Response(
                {"detail": "User does not exist",
                 "type": "error"}, status=status.HTTP_404_NOT_FOUND)
        is_correct_password = check_password(password=request.data['password'],
                                           encoded=user.password)
        if not is_correct_password:
            return Response(
                {"detail": "Password wrong",
                 "type": "error"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Ensure only one token per user
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        
        return Response({
            "detail": "Login successful",
            "type": "success",
            "token": token.key
        }, status=status.HTTP_200_OK)
    return Response({"Errors": serializer.errors,
                     "type": "error",
                     "detail": "Missing Fields"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def sign_up(request: Request) -> Response:
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        
        email = request.data.get('email')
                
        # Check if a user with the provided email already exists
        exists = User.objects.filter(email=email).exists()
        if exists:
            return Response({"detail": "User with this email already exists",
                             "type": "error"}, status=status.HTTP_400_BAD_REQUEST)
        exists = User.objects.filter(username=request.data.get('username')).exists()
        password = request.data['password']
        hashed_password = make_password(password)
        
        user = User.objects.create(email=email, password=hashed_password,
                                        first_name=request.data['first_name'],
                                        last_name=request.data['last_name'],
                                        username=request.data['username'])
        token = Token.objects.create(user=user)        
        serializer.data.pop("password")
        return Response({
            "token": token.key, 
            "user": serializer.data,
            "type": "success",
            "detail": "User created successfully"
        }, status=status.HTTP_201_CREATED)

    return Response({"Errors": serializer.errors,
                     "type": "error",
                     "detail": "Missing Fields"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def token_test(request: Request) -> Response:
    return Response({"detail": "Access granted!"},
                    status=status.HTTP_400_BAD_REQUEST)