from django.shortcuts import render
from rest_framework.decorators import api_view
from app.models import Department
from rest_framework.response import Response
from app.serializers import DepartmentSerializer


@api_view(["GET", "POST"])
def get_or_create_department(request):
    if request.method == "GET":
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)