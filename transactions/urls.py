from django.urls import path, re_path
from transactions import views

urlpatterns = [
    path('transaction/', views.index),
    path('<str:filter>/<str:filterVariable>/', views.TransactionView.as_view()),
]