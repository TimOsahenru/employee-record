from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name
    
    
class Employee(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    salary = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    