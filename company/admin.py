from django.contrib import admin
from django.conf import settings
from .models import *
# Register your models here.

class CompanyAdmin(admin.ModelAdmin):
    list_display=("user","name","logo","email","password","port","smtp","active","key")

class CourseAdmin(admin.ModelAdmin):
    list_display=("company","name","description","active")

class SigneeAdmin(admin.ModelAdmin):
    list_display=("course","name","signature","job_title","active")

class CertificateAdmin(admin.ModelAdmin):
    list_display=("course","student_name","student_last_name","student_id","student_email","date_of_course","signature_date")

admin.site.register(Company, CompanyAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Signee, SigneeAdmin)
admin.site.register(Certificate, CertificateAdmin)



