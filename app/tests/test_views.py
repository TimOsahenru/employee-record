from rest_framework.test import APITestCase
from app.models import Department, Employee
from django.urls import reverse
from app.serializers import DepartmentSerializer
from rest_framework import status


class DepertmentAPITest(APITestCase):
    def setUp(self):
        self.get_create_url = reverse("get_or_create_department")
        self.departments = [
            {"name": "Accounting"},
            {"name": "Engineering"},
            {"name": "Socials"},
        ]
        
        for department_data in self.departments:
            Department.objects.create(name=department_data["name"])
        
            
    def test_can_get_all_departments(self):
        response = self.client.get(self.get_create_url)
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(departments), 3)
        
    def test_can_create_departments(self):
        response = self.client.post(self.get_create_url, data=self.departments[0], format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, "Added successfully")
        
    def test_cannot_create_department_without_name(self):
        response = self.client.post(self.get_create_url, {}, format="json")
        serializer = DepartmentSerializer(data={})
        serializer.is_valid()
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, serializer.errors)
        
    def test_can_get_departments_by_id(self):
        department = Department.objects.create(name="Engineering")
        url = reverse("update_or_delete_department", args=[department.id])
        
        response = self.client.get(url)
        serializer = DepartmentSerializer(department)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual("Engineering", department.name)
        
    def test_cannot_get_a_department_that_does_not_exist(self):
        url = reverse("update_or_delete_department", args=[1096])
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Department does not exist")
        
    def test_can_update_department(self):
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
        
    def test_cannot_update_department_that_does_not_exist(self):
        department = Department.objects.create(name={})
        url = reverse("update_or_delete_department", args=[department.id])
        
        response = self.client.put(url, {}, format="json")
        department.refresh_from_db()
        
        serializer = DepartmentSerializer(data={})
        serializer.is_valid()
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, serializer.errors)
        
        
    def test_can_delete_department_with_name(self):
        department = Department.objects.create(name="Human relations")
        url = reverse("update_or_delete_department", args=[department.id])
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Deleted successfully")
        # 4 objects created 3 from the setUp method 1 from this method function
        # deleting 1 will be left with 3
        self.assertEqual(Department.objects.count(), 3)
        
        
    def test_cannot_delete_department_that_does_not_exist(self):
        url = reverse("update_or_delete_department", args=[100])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Department does not exist")
        
        
class EmployeeAPITest(APITestCase):
    def setUp(self):
        self.create_employee_url = reverse("get_all_employee_or_create_employee")
        self.department = Department.objects.create(name="Accounting")
        self.employee_data = [
            {
                "name": "Tim Osahenru",
                "age": 28,
                "salary": 3000,
                "department": self.department
            },
            {
                "name": "John Stewart",
                "age": 34,
                "salary": 6000,
                "department": self.department
            },
            {
                "name": "Peter Simeon",
                "age": 25,
                "salary": 4000,
                "department": self.department
            }
        ]
        
        for data in self.employee_data:
            Employee.objects.create(**data)
            
            
    def test_get_all_employees(self):
        response = self.client.get(self.create_employee_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.employee_data))
        
    def test_can_create_employee(self):
        data = {
            "name": "Peter Simeon",
            "age": 25,
            "salary": 4000,
            "department": self.department.pk
            }
        response = self.client.post(self.create_employee_url, data, format="json")