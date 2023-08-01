from django.shortcuts import render
from rest_framework.decorators import api_view
from app.models import Department
from rest_framework.response import Response
from app.serializers import DepartmentSerializer
from rest_framework import status


@api_view(["GET", "POST"])
def get_or_create_department(request):
    if request.method == "GET":
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)
    
    if request.method == "POST":
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({}, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)