from rest_framework.test import APITestCase
from app.models import Department, Employee
from django.urls import reverse
from app.serializers import DepartmentSerializer
from rest_framework import status


class DepertmentAPITest(APITestCase):
    def setUp(self):
        self.url = reverse("get_or_create_department")
    
    def test_get_departments(self):
        department_1 = Department.objects.create(name="Accounting")
        department_2 = Department.objects.create(name="Finance")
        
        response = self.client.get(self.url)
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)