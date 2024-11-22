from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from . import api

app_name="main"
urlpatterns = [
    # Authentication
    path('', views.index, name="index"),
    path('register/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account_details, name="account_details"),
    path('account/changepassword/', views.change_password, name="changepassword"),
    

    # Member Dashboard and Actions
    path('member/', views.member_dashboard, name='member_dashboard'),
    path('member/update-profile/', views.update_member_profile, name='update_member_profile'),
    path('member/payment-history/', views.member_payment_history, name='member_payment_history'),
    path('member/claim/create/', views.create_claim, name='create_claim'),
    path('member/claim/list/', views.claims_list, name='claim_list'),
    path('member/claim/update/<int:claim_id>', views.update_claim, name='update_claim'),

    path('member/beneficiary/list/', views.beneficiary_list, name='beneficiary_list'),
    path('member/beneficiary/add/', views.add_beneficiary, name='add_beneficiary'),
    path('member/beneficiary/update/<int:beneficiary_id>/', views.update_beneficiary, name='update_beneficiary'),
    path('member/beneficiary/delete/<int:beneficiary_id>/', views.delete_beneficiary, name='delete_beneficiary'),
    

    # Trustee Dashboard and Actions
    path('trustee/', views.trustee_dashboard, name='trustee_dashboard'),
    path('trustee/analytics/', views.trustee_analytics, name='trustee_analytics'),

    path('trustee/create/<int:member_id>/', views.create_trustee, name='create_trustee'),
    path('trustee/update/<int:trustee_id>/', views.update_trustee, name='update_trustee'),
    path('trustee/delete/<int:trustee_id>/', views.delete_trustee, name='delete_trustee'),

    path('trustee/claim/list/', views.trustee_claim_list, name='trustee_claim_list'),
    path('trustee/claim/<int:claim_id>/', views.claiminfo, name='claim_info'),
    path('trustee/claim/approve/<int:claim_id>/', views.approve_claim, name='approve_claim'),
    path('trustee/claim/reject/<int:claim_id>/', views.reject_claim, name='reject_claim'),
    path('trustee/settings/', views.trustee_settings, name="trustee_settings"),

    #path('trustee/beneficiary/<int:beneficiary_id>', views.beneficiaryinfo, name='beneficiary_info'),
    
    path('trustee/member/list/', views.member_list, name='member_list'),
    #path('trustee/member/update-payment/<int:member_id>/', views.update_payment_status, name='update_payment'),
    path('trustee/member/add-payment/<int:member_id>/', views.add_payment, name="add_payment"),
    path('trustee/member/info/<int:member_id>/', views.member_info, name='member_info'),
    path('trustee/member/delete/<int:member_id>/', views.member_delete, name='delete_member'),


    # ANALYTICS API
    path("api/trends/", api.trends_view, name='trends_api'),
    path("download/claims/", api.claims_export, name="claims_download"),
    path("download/beneficiaries/", api.beneficiaries_export, name="beneficiaries_download"),
    path("download/members/", api.members_export, name="members_download"),
    path("download/contributions/", api.contributions_export, name="contributions_download"),

] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)