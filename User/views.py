from cryptography.fernet import Fernet
from django.shortcuts import redirect, render
from User.models import *
from company.models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import smtplib, ssl, sys, getpass, hashlib, webbrowser, random, base64, uuid, cryptocode
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.conf import settings

# REGISTRATION OF A USER

def index(request):
    return render(request,"index.html")

def handle_not_found(request,exception):
    return render(request,"not_found.html")

def handle_error_500(request):
    return render(request,"handle_error_500.html")

def faq(request):
    return render(request,"faq.html")

def signup(request):
    if request.user.is_authenticated:
        return redirect('../dashboard/'+str(request.user.id))
    return render(request,"signup.html")

def user_registered(request):
    first_name=request.POST["first_name"]
    last_name=request.POST["last_name"]
    email=request.POST["email"]
    has_email=User.objects.filter(email=email)
    if has_email:
        return JsonResponse({'success':False,'error_message':"El correo electrónico ya se encuentra registrado en la base de datos"})
    password=request.POST["password"]

    new_user=User()
    new_user.username=email
    new_user.first_name=first_name
    new_user.last_name=last_name
    new_user.email=email
    new_user.set_password(password)

    new_user.save()

    new_profile=Profile()
    new_profile.user=new_user
    new_profile.first_name=first_name
    new_profile.last_name=last_name
    new_profile.on_hold_user=True
    new_profile.active=False
    new_profile.confirmation_code = random.randint(134560,301648)
    new_profile.save()
    subject='Confirmá tu correo electrónico'
    text = 'Tu código de activación es: ' + str(new_profile.confirmation_code) + ' . Para activarla hacé click en el siguiente link: https://generadordecertificados.herokuapp.com/activate_account/.'
    html = """\
    <html>
    <head></head>
    <body>
        <p>Tu código de activación es: {activation_code}. Copialo y activá tu cuenta haciendo click <a href="https://generadordecertificados.herokuapp.com/activate_account/">acá</a>.
        </p>
    </body>
    </html>
    """.format(activation_code=new_profile.confirmation_code)
    send_confirmation_code(email,subject,text,html)
    return JsonResponse({'success':True,'email':new_profile.user.email,'id':new_profile.id})

def send_confirmation_code(email,subject,text,html):
    host = "smtp.gmail.com"
    port = 587
    sender = 'generadordecertificados@gmail.com'
    password = settings.EMAIL_PASSWORD
    receiver = email

    email_conn = smtplib.SMTP(host, port)
    email_conn.ehlo()
    email_conn.starttls()
    email_conn.login(sender, password)

    the_msg = MIMEMultipart("alternative")
    the_msg['Subject'] = subject
    the_msg['From'] = str('Generador de Certificados <sender>')
    the_msg['To'] = receiver

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    the_msg.attach(part1)
    the_msg.attach(part2)

    email_conn.sendmail(sender, receiver, the_msg.as_string())
    email_conn.close()

def activate_account(request):
    return render(request,"activate_account.html")

def account_activation(request):
    email=request.POST["email"]
    activation_code=request.POST["activation_code"]

    try:
        user_email=User.objects.get(email=email)
        profile=Profile.objects.get(user=user_email)
    except:
        return render(request,"non_existing_user_password.html")

    if str(profile.confirmation_code) == activation_code and profile.on_hold_user == False:
        return redirect('../login/')

    elif str(profile.confirmation_code) == activation_code:
        profile.on_hold_user=False
        profile.active=True
        profile.save()
        return render(request,"activated_user.html")
    elif str(profile.confirmation_code) != activation_code and profile.on_hold_user == False:
        return render(request,"invalid_code_account_activated.html")
    else:
        return render(request,"invalid_code.html")

def resend_account_activation(request):
    profile_id = request.GET["id"]
    profile=Profile.objects.get(id=profile_id)
    profile.confirmation_code = random.randint(134560,301648)
    profile.save()

    subject='Confirmá tu correo electrónico (nuevo código)'
    text = 'Tu nuevo código de activación es: ' + str(profile.confirmation_code) + ' . Para activarla hacé click en el siguiente link: http://127.0.0.1:8000/activate_account/.'
    html = """\
    <html>
    <head></head>
    <body>
        <p>Tu nuevo código de activación es: {activation_code}. Copialo y activá tu cuenta desde click <a href="http://127.0.0.1:8000/activate_account/">acá</a>.
        </p>
    </body>
    </html>
    """.format(activation_code=profile.confirmation_code)

    send_confirmation_code(profile.user.email,subject,text,html)
    return redirect('../activate_account/?email='+profile.user.email+'&id='+str(profile.id))

def login_page(request):
    if request.user.is_authenticated:
        return redirect('../dashboard/'+str(request.user.id))
    return render(request,"login.html")

# def google_login(request):
#     return redirect('../dashboard/'+str(request.user.id))

def logoutUser(request):
    logout(request)
    return redirect('../login/')

def check_credentials(request):

    username=request.POST.get('email')
    password=request.POST.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        profile=Profile.objects.get(user=user)
        if profile.active == False:
            return render(request,"deleted_user.html",{"profile":profile})
        if profile.on_hold_user == False:
            login(request,user)
            return redirect('../dashboard/'+str(user.id))

        else:
            return render(request,"activate_account_verification.html",{"profile":profile})
    else:
        return render(request,"non_existing_user_password.html")

@login_required(login_url='../login/')
def dashboard(request, user_id):
    user=User.objects.get(id=user_id)
    companies=Company.objects.filter(user__id=user_id,active=True)
    companies_not_active=Company.objects.filter(user__id=user_id,active=False)
    if user != request.user:
        context = {
            logout(request)
        }
        return render(request,"not_allowed.html",{"context":context})
    else:
        return render(request,"dashboard.html",{"companies":companies,
        "companies_not_active":companies_not_active})

def delete_user(request):
    id=request.GET["id"]
    user=User.objects.get(id=id)
    profile=Profile.objects.get(user=user)
    profile.active=False
    profile.on_hold_user=True
    profile.save()
    if user != request.user:
        context = {
            logout(request)
        }
        return render(request,"not_allowed.html",{"context":context})
    else:
        return JsonResponse({'success':True})

def reactivate_user(request):
    id=request.GET["id"]
    profile=Profile.objects.get(id=id)
    profile.active=True
    profile.on_hold_user=False
    profile.save()
    return render(request,"reactivated_user.html")

@login_required(login_url='../login/')
def modify_user(request):
    id=request.GET["id"]
    user=User.objects.get(id=id)
    if user != request.user:
        context = {
            logout(request)
        }
        return render(request,"not_allowed.html",{"context":context})
    else:
        return render(request,"modify_user.html",{"user":user})

@login_required(login_url='../login/')
def user_modification(request):
    id=request.POST.get('id')
    first_name=request.POST.get('first_name')
    last_name=request.POST.get('last_name')
    email=request.POST.get('email')
    user_id=User.objects.get(id=id)
    emails=User.objects.filter(email=email).count()
    if emails > 0 and user_id.email != email:
        return render(request,"existing_email.html")

    modify_user=User.objects.get(id=id)
    modify_user.first_name=first_name
    modify_user.last_name=last_name
    modify_user.email=email
    modify_user.save()
    return render(request,"modified_user.html",{"modify_user":modify_user})


def recover_password(request):
    return render(request,"recover_password.html")

def password_recovery(request):
    email=request.POST.get("email")
    try:
        user=User.objects.get(email=email)
    except:
        return render(request,"not_existing_email.html")
    profile=Profile.objects.get(user=user)
    profile.confirmation_code = random.randint(134560,301648)
    profile.save()
    subject='Recuperá tu contraseña'
    text = 'Hacé click en el siguiente link: https://generadordecertificados.herokuapp.com/password_recovery_final/?id='+str(user.id)+'&confirmation_code='+str(profile.confirmation_code) + ' para recuperar tu contraseña.'
    html = """\
    <html>
    <head></head>
    <body>
        <p>Para recuperar tu contraseña hace click <a href='https://generadordecertificados.herokuapp.com/password_recovery_final/?id={user_id}&confirmation_code={confirmation_code}'>acá</a>.
        </p>
    </body>
    </html>
    """.format(user_id=user.id,confirmation_code=profile.confirmation_code)
    send_confirmation_code(user.email,subject,text,html)
    return render(request,"password_sent.html",{"id":user.id})

def password_recovery_final(request):
    id=request.GET["id"]
    user=User.objects.get(id=id)
    return render(request,"password_recovery_final.html",{"user":user})

def password_changed(request):
    email=request.POST["email"]
    password=request.POST["password"]
    confirmation_code=request.POST["confirmation_code"]
    user=User.objects.get(email=email)
    profile=Profile.objects.get(user=user)
    if int(confirmation_code) == profile.confirmation_code:
        user.set_password(password)
        user.save()
        return JsonResponse({'success':True})
    else:
        return JsonResponse({'success':False})

