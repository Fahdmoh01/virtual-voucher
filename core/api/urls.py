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
    # add participant to event
	path("add-participant/", views.AddEventParticipantAPI.as_view(), name="add_participant"),
    # remove participant from event
	path("rem-participant/", views.RemoveParticipant.as_view(), name="rem_particpant"),
]


#vouchers 
urlpatterns +=[
    #Gets all vouchers created by user
	path('all-vouchers/',views.VoucherListAPI.as_view(), name="all-vouchers"),
	#create, update, delete voucher
	path('cud-voucher/',views.CUDVoucherAPI.as_view(), name='cud_voucher'),
	#get system statistics
	path("stats/",views.SystemStatsAPI.as_view(), name="stats"),
	#revoke redeemer's ability to redeem a voucher
	path("revoke-redeemer/", views.RevokeRedeemersVoucherAPI.as_view(), name="revoke_redeemer"),
	#redeems user's voucher
	path("redeem-voucher/", views.RedeemVoucherApI.as_view(), name="redeem_vouhcer"),
    #sends vouchers to event participant
	path("broadcast-voucher/", views.BroadcastVoucherAPI.as_view(), name="broad_cast"),
]