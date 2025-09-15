from django.urls import path
from .views import import_data, register, check_eligibility, create_loan, view_loan, view_loans

urlpatterns = [
    path('import-data/', import_data),
    path('register/', register),
    path('check-eligibility/', check_eligibility),
    path('create-loan/', create_loan),
    path('view-loan/<int:loan_id>/', view_loan),
    path('view-loans/<int:customer_id>/', view_loans),
]
