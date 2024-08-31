from django.urls import path
from transactions import views

urlpatterns = [
    path('<str:filter>/<str:filterVariable>/', views.TransactionView.as_view(), name='transaction_view'),
]