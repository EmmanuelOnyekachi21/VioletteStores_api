from django.shortcuts import render
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['POST'])
def register_user(request):
    try:
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": "User Created Successfully",
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)