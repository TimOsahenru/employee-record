from django.urls import path
from app import views


urlpatterns = [
 path("", views.get_or_create_department, name="get_or_create_department"),
 path("update_or_delete_department/<str:id>/", views.update_or_delete_department, name="update_or_delete_department"),
 path("get_or_create_employee", views.get_or_create_employee, name="get_all_employee_or_create_employee"),
 path("update_or_delete_employee/<str:id>/", views.update_or_delete_employee, name="update_or_delete_employee")
]
