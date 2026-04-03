from django.urls import path
from . import views

app_name = "vmb"
urlpatterns = [
    # Basic pages
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("instrument/", views.instrument, name="instrument"),
    path("uniform/", views.uniform, name="uniform"),

    # Database pages
    path("database/", views.database, name="database"),
    path("database/member_db/", views.member_db, name="member_db"),
    path("database/uniform_db/", views.uniform_db, name="uniform_db"),
    path("database/uniform_rental_db", views.uniform_rental_db, name="uniform_rental_db"),
    path("database/instrument_db/", views.instrument_db, name="instrument_db"),
    path("database/instrument_rental_db", views.instrument_rental_db, name="instrument_rental_db"),

    # Member API endpoints
    path('member/update/<str:pk>/', views.update_member, name='update_member'),
    path('member/delete/<str:pk>/', views.delete_member, name='delete_member'),
    path('member/add/', views.add_member, name='add_member'),

    # Uniform API endpoints
    path('uniform/update/<str:pk>/', views.update_uniform, name='update_uniform'),
    path('uniform/delete/<str:pk>/', views.delete_uniform, name='delete_uniform'),
    path('uniform/add/', views.add_uniform, name='add_uniform'),

    # Instrument API endpoints
    path('instrument/update/<str:pk>/', views.update_instrument, name='update_instrument'),
    path('instrument/delete/<str:pk>/', views.delete_instrument, name='delete_instrument'),
    path('instrument/add/', views.add_instrument, name='add_instrument'),
]