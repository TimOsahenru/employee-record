from django.urls import path
from app import views


urlpatterns = [
 path("", views.get_or_create_department, name="get_or_create_department"),
 path("update_or_delete/<str:id>/", views.update_or_delete_department, name="update_or_delete_department")
]
