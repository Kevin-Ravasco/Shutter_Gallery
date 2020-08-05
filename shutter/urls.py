from django.urls import path
from shutter.views import home, photos, profile, contact, update_album, delete_album, delete_album_page

urlpatterns = [
    path('', home, name='home'),
    path('photos/<int:id>/', photos, name='photos'),
    path('profile/', profile, name='profile'),
    path('contact/', contact, name='contact'),
    path('update/<int:id>/', update_album, name='update_album'),
    path('delete_album/<int:id>/', delete_album_page, name='delete_album_page'),
    path('delete/<int:id>/', delete_album, name='delete_album'),

]


# Allauth views
'''
urlpatterns = [
    path("signup/", views.signup, name="account_signup"),
    path("login/", views.login, name="account_login"),
    path("logout/", views.logout, name="account_logout"),
    path("password/change/", views.password_change,
         name="account_change_password"),
    path("password/set/", views.password_set, name="account_set_password"),
    path("inactive/", views.account_inactive, name="account_inactive"),

    # E-mail
    path("email/", views.email, name="account_email"),
    path("confirm-email/", views.email_verification_sent,
         name="account_email_verification_sent"),
    re_path(r"^confirm-email/(?P<key>[-:\w]+)/$", views.confirm_email,
            name="account_confirm_email"),

    # password reset
    path("password/reset/", views.password_reset,
         name="account_reset_password"),
    path("password/reset/done/", views.password_reset_done,
         name="account_reset_password_done"),
    re_path(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
            views.password_reset_from_key,
            name="account_reset_password_from_key"),
    path("password/reset/key/done/", views.password_reset_from_key_done,
         name="account_reset_password_from_key_done"),
]

'''