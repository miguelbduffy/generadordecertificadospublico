from django.db import models
from User.models import User
from django.core.exceptions import ValidationError
from PIL import Image
from django.conf import settings

def maximum_size(width=None, height=None):
    def validator(image):
        img = Image.open(image)
        fw, fh = img.size
        if fw > width or fh > height:
            raise ValidationError(
            "Height or Width is larger than what is allowed")
    return validator

class Company(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    logo = models.ImageField(null=True,blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=300)
    port = models.IntegerField()
    smtp = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    key = models.CharField(max_length=500)


    def __str__(self):
        return self.name

class Course(models.Model):
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=500,verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Signee(models.Model):
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=500,verbose_name="Nombre")
    signature = models.ImageField(verbose_name="Firma")
    job_title = models.CharField(max_length=100,verbose_name="Puesto laboral")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Certificate(models.Model):
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100,verbose_name="Nombre")
    student_last_name = models.CharField(max_length=100,verbose_name="Apellido")
    student_id = models.CharField(max_length=20,verbose_name="DNI")
    student_email = models.EmailField()
    date_of_course = models.CharField(max_length=20,null=True, blank=True, verbose_name="Fecha del curso")
    signature_date = models.CharField(max_length=20,null=True, blank=True, verbose_name="Fecha del firmante")

    def __str__(self):
        return self.student_name


