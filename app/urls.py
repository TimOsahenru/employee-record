from django.urls import path
from app import views


urlpatterns = [
 path("", views.get_or_create_department, name="get_or_create_department")
]
