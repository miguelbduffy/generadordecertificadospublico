from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include, url
from User import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView


urlpatterns = [
    
    path('company/', include('company.urls')),
    path('social_app/', include('social_app.urls')),

    path('admin/', admin.site.urls),

    #HOMEPAGE
    path('', views.index, name="Index"),
    path('faq/',views.faq, name="FAQ"),

    #SIGN UP
    path('', TemplateView.as_view(template_name="index.html")),
    path('accounts/', include('allauth.urls')),#SOCIAL APPS
    path('signup/',views.signup, name="Sign up"),#MANUAL SIGN UP
    path('user_registered/',views.user_registered, name="User has been registered"),
    path('activate_account/',views.activate_account, name="Activate account"),#ACTIVATE ACCOUNT
    path('account_activation/',views.account_activation, name="Account activation"),#ACCOUNT ACTIVATION
    path('resend_account_activation/',views.resend_account_activation, name="Resend activation code"),#RESEND ACTIVATION CODE
    path('dashboard/<int:user_id>',views.dashboard, name="Dashboard"),#DASHBOARD
    
    #LOGIN AND LOGOUT
    path('login/',views.login_page, name="Login"),#LOGIN
    # path('google_login/', views.google_login, name='google_login'),
    path('logout/',views.logoutUser, name="Logout"),#LOGOUT
    path('check_credentials/',views.check_credentials, name="Check credentials"),#CHECK CREDENTIALS
    path('recover_password/', views.recover_password, name="Recover password"),#RECOVER PASSWORD
    path('password_recovery/', views.password_recovery, name="Password recovery"),#PASSWORD RECOVERY
    path('password_recovery_final/', views.password_recovery_final, name="Password recovery final"),#PASSWORD RECOVERY FINAL
    path('password_changed/', views.password_changed, name="Password changed"),#PASSWORD CHANGED


    #DELETE/MODIFY USER
    path('delete_user',views.delete_user, name="Delete user"),
    path('reactivate_user',views.reactivate_user, name="Reactivate user"),
    path('modify_user',views.modify_user, name="Modify user"),
    path('user_modification',views.user_modification, name="User modification"),
    
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404="User.views.handle_not_found"
handler500="User.views.handle_error_500"
