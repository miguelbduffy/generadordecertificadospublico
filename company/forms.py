from django.forms import ModelForm, widgets
from django import forms
from .models import Company, Course, Signee

class DateInput(forms.DateInput):
    input_type = 'date'

class CreateCompanyForm(ModelForm):
    class Meta:
        model=Company
        fields='__all__'
        exclude=('user','active','logo')
        widgets = {
            'password': forms.PasswordInput(),
        }

class CreateCourseForm(ModelForm):
    class Meta:
        model=Course
        fields='__all__'
        exclude=('company','active','date_of_course')
        widgets = {
            'date_of_course': DateInput()
        }

class CreateSigneeForm(ModelForm):
    class Meta:
        model=Signee
        fields='__all__'
        exclude=('course','signature_date','active')