from django.db import models
import datetime

class Student(models.Model):
    # Personal Info
    FullName = models.CharField(max_length=20)
    FatherName = models.CharField(max_length=20)
    Gender = models.CharField(max_length=10)
    BirthDate = models.DateField()
    Address = models.CharField(max_length=100)
    City = models.CharField(max_length=20)
    State = models.CharField(max_length=20)
    Mobile = models.CharField(max_length=10)
    Password = models.CharField(max_length=12)

    # Academic Info
    CollegeID = models.CharField(max_length=10)
    CollegeName = models.CharField(max_length=20)
    EnrollNum = models.CharField(max_length=15, unique=True)

    # Unique Info
    RFID = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.EnrollNum + ' | ' + self.FullName

    class Meta:
        db_table = "Student"

class Seller(models.Model):
    # Seller Info
    RFID = models.CharField(max_length=20, primary_key=True)
    RegDate = models.DateField()
    OwnerName = models.CharField(max_length=20,null=True)
    Company = models.CharField(max_length=20,null=True)
    Mobile = models.CharField(null=True,max_length=10)
    Address = models.CharField(null=True,max_length=100)
    Type = models.CharField(max_length=20,null=True)
    About = models.CharField(max_length=100,null=True)
    Password = models.CharField(max_length=12)

    class Meta:
        db_table = "Seller"

class Product(models.Model):
    # Product Info
    RFID = models.CharField(max_length=20)
    ProductID = models.CharField(max_length=20, unique=True)
    ProductName = models.CharField(max_length=20)
    Category = models.CharField(max_length=20)
    Price = models.CharField(max_length=20)
    Description = models.TextField(max_length=100)

    class Meta:
        db_table = "Product"