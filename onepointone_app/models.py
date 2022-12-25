from django.db import models

# Create your models here.

class LoginDetails(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    created_at= models.DateTimeField()

    def __str__(self):
        return self.username

    class Meta:
        managed = True
        db_table = "login"


class EmployeeData(models.Model):
    id = models.AutoField(primary_key=True)
    emp_id = models.CharField(max_length=100,null=True, blank=True)
    name = models.CharField(max_length=100)
    dob = models.CharField(max_length=50)
    doj = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    manager = models.CharField(max_length=50)
    picture = models.FileField(upload_to="pic/", null=True, blank=True)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length = 254)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = "employee_data"