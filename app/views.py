from django.shortcuts import render
from rest_framework.decorators import api_view


@api_view(["GET", "POST"])
def get_or_create_department(request):
    pass