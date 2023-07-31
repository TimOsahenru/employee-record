from rest_framework.test import APITestCase
from app.models import Department, Employee
from django.urls import reverse


class DepertmentAPITest(APITestCase):
    def setUp(self):
        # self.department_data = Department.objects.create(name="Engineering")
        self.url = reverse("get_or_create_department")
    
    def test_get_departments(self):
        pass
        # department_1 = Department.objects.create("Accounting")
        # department_2 = Department.objects.create("Finance")