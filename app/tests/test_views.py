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
            self.assertEqual(response.data, "Added successfully")
        self.assertEqual(Department.objects.count(), 3)
        
    def test_create_department_with_missing_name(self):
        response = self.client.post(self.get_create_url, {}, format="json")
        serializer = DepartmentSerializer(data={})
        serializer.is_valid()
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, serializer.errors)
        
    def test_update_department(self):
        department = Department.objects.create(name="Socials")
        url = reverse("update_or_delete_department", args=[department.id])
        updated_data = {
            "name": "Engineering"
        }
        
        response = self.client.put(url, data=updated_data, format="json")
        department.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Updated successfully")
        self.assertEqual(department.name, updated_data["name"])
        
    def test_update_department_does_not_exist(self):
        department = Department.objects.create(name={})
        url = reverse("update_or_delete_department", args=[department.id])
        
        response = self.client.put(url, {}, format="json")
        department.refresh_from_db()
        
        serializer = DepartmentSerializer(data={})
        serializer.is_valid()
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, serializer.errors)
        
        
    def test_delete_department(self):
        department = Department.objects.create(name="Human relations")
        url = reverse("update_or_delete_department", args=[department.id])
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Deleted successfully")
        self.assertEqual(Department.objects.count(), 0)
        
        
    def test_delete_department_that_does_not_exist(self):
        url = reverse("update_or_delete_department", args=[1])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Department does not exist")