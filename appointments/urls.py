from django.urls import path
from .views import book_appointment  # patient view only
from . import views
urlpatterns = [
    path('book/', book_appointment, name='book_appointment'),
    path('confirm/<int:appointment_id>/', views.confirm_appointment, name='confirm_appointment'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
]
