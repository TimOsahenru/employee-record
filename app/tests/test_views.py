from rest_framework.test import APITestCase
from app.models import Department, Employee
from django.urls import reverse
from app.serializers import DepartmentSerializer
from rest_framework import status


class DepertmentAPITest(APITestCase):
    def setUp(self):
        self.get_create_url = reverse("get_or_create_department")
        self.departments_data = [
            {"name": "Accounting"},
            {"name": "Engineering"},
            {"name": "Socials"},
        ]
        
    def test_get_departments(self):
        for department_data in self.departments_data:
            Department.objects.create(name=department_data["name"])
    
        response = self.client.get(self.get_create_url)
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(departments), 3)
        
    def test_create_departments(self):
        for data in self.departments_data:
            response = self.client.post(self.get_create_url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {})
        
        
    def test_update_or_delete_department(self):
        department = Department.objects.create(name="Socials")
        url = reverse("update_or_delete_department", args=[department.id])
        updated_data = {
            "name": "Engineering"
        }
        
        response = self.client.put(url, data=updated_data, format="json")
        department.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})
        self.assertEqual(department.name, updated_data["name"])