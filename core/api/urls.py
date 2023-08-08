from knox import views as knox_views
from django.urls import path
from . import views

# authentication
urlpatterns = [
    # API Overview
    path("", views.OverviewAPI.as_view(), name="api-overview"),
    # signup a new user
    path('sign-up/', views.SignUpAPI.as_view(), name="sign_up"),
    # login users
    path('login/', views.LoginAPI.as_view(), name="login"),
    # logout user
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    # logout user from all sessions
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]

# events
urlpatterns += [
    # Gets all events created by user
    path("all-events/", views.EventListAPI.as_view(), name="all_events"),
    # create, update, delete event
    path("cud-event/", views.CUDEventAPI.as_view(), name="cud_event"),
]


#vouchers 
urlpatterns +=[
    #Gets all vouchers created by user
	path('all-vouchers/',views.VoucherListAPI.as_view(), name="all-vouchers"),
    #create, update, delete voucher
	path('cud-voucher/',views.CUDVoucherAPI.as_view(), name='cud_voucher'),
]