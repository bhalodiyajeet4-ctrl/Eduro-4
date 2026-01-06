from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import AdminUser, Teacher, Student
from .serializers import LoginSerializer, AdminUserSerializer, TeacherSerializer, StudentSerializer


class AdminLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = AdminUser.objects.get(email=email, is_active=True)
            if user.check_password(password):
                refresh = RefreshToken()
                refresh['user_id'] = user.id
                refresh['user_type'] = 'ADMIN'
                refresh['email'] = user.email

                return Response({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'user_type': 'ADMIN',
                    'user': AdminUserSerializer(user).data
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except AdminUser.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class TeacherLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = Teacher.objects.get(email=email, is_active=True)
            if user.check_password(password):
                refresh = RefreshToken()
                refresh['user_id'] = user.id
                refresh['user_type'] = 'TEACHER'
                refresh['email'] = user.email

                return Response({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'user_type': 'TEACHER',
                    'user': TeacherSerializer(user).data
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Teacher.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class StudentLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = Student.objects.get(email=email, is_active=True)
            if user.check_password(password):
                refresh = RefreshToken()
                refresh['user_id'] = user.id
                refresh['user_type'] = 'STUDENT'
                refresh['email'] = user.email

                return Response({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'user_type': 'STUDENT',
                    'user': StudentSerializer(user).data
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Student.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
