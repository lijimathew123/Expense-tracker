from django.urls import path
from . import views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('create/', views.create_expense, name='create_expense'),
    
    path('report/', views.expense_report, name='expense_report'),
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
]
