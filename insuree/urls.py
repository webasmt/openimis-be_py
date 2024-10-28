from django.urls import path
from . import views

urlpatterns = [
    path('insuree/create/', views.create_insuree_with_photo, name='create_insuree_with_photo'),
    path('insuree/<int:insuree_id>/photo', views.delete_insuree_photo, name='delete_insuree_photo'),
]