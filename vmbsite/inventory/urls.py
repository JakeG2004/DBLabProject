from django.urls import path
from . import views

app_name = "vmb"
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("instrument/", views.instrument, name="instrument"),
    path("uniform/", views.uniform, name="uniform"),
    path("database/", views.database, name="database"),
    path("database/member_db/", views.member_db, name="member_db"),
    path("database/uniform_db/", views.uniform_db, name="uniform_db"),
    path("database/instrument_db/", views.instrument_db, name="instrument_db"),
]