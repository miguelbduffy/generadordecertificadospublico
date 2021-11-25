from django.urls import path
from company import views
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
#CHOOSE/CREATE/MODIFY/DELETE/REACTIVATE COMPANY
    path('create/<int:user_id>',views.create_company, name="Create company"),#CREATE COMPANY
    path('company_creation',views.company_creation, name="Company creation"),#COMPANY CREATION
    path('modify_company',views.modify_company, name="Modify company"),#MODIFY COMPANY
    path('company_modification',views.company_modification, name="Company modification"),#COMPANY MODIFICATION
    path('delete_company',views.delete_company, name="Delete company"),#DELETE COMPANY
    path('reactivate_company',views.reactivate_company, name="Reactivate company"),#REACTIVATE COMPANY

#CHOOSE/CREATE/MODIFY/DELETE COURSE
    path('choose_course',views.choose_course, name="Choose course"),#CHOOSE COURSE
    path('create_course',views.create_course,name="Create course"),#CREATE COURSE
    path('course_creation',views.course_creation,name="Course creation"),#COURSE CREATION
    path('modify_course',views.modify_course,name="Modify course"),#MODIFY COURSE
    path('course_modification',views.course_modification,name="Course modification"),#COURSE MODIFICATION
    path('delete_course',views.delete_course,name="Delete course"),#DELETE COURSE
    path('delete_course_confirmation',views.delete_course_confirmation,name="Delete course confirmation"),#DELETE COURSE CONFIRMATION
    path('reactivate_course',views.reactivate_course, name="Reactivate course"),#REACTIVATE COURSE

#CHOOSE/CREATE/MODIFY/DELETE SIGNEE
    path('choose_signee',views.choose_signee, name="Choose signee"),#CHOOSE SIGNEE
    path('create_signee',views.create_signee, name="Create signee"),#CREATE SIGNEE
    path('modify_signee',views.modify_signee, name="Modify signee"),#MODIFY SIGNEE
    path('modified_signee',views.modified_signee, name="Modified signee"),#MODIFIED SIGNEE
    path('delete_signee',views.delete_signee, name="Delete signee"),#DELETE SIGNEE
    # path('signee_deletion',views.signee_deletion, name="Signee deletion"),#SIGNEE DELETION
    path('reactivate_signee',views.reactivate_signee, name="Reactivate signee"),#REACTIVATE SIGNEE
    
#CHOOSE/CREATE CERTIFICATE
    path('upload_excel',views.upload_excel, name="Upload Excel"),#UPLOAD EXCEL
    path('import_excel',views.import_excel, name="Import Excel"),#IMPORT EXCEL

#SEND CERTIFICATE
    path('enviar_certificado',views.send_certificate, name="Send Certificate"),#SEND CERTIFICATE

]