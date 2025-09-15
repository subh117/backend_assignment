from celery import shared_task
import pandas as pd
from .models import Customer, Loan
from datetime import datetime

@shared_task
def import_customers_and_loans():
    customers = pd.read_excel('customer_data.xlsx')
    loans = pd.read_excel('loan_data.xlsx')
    
    for _, row in customers.iterrows():
        Customer.objects.update_or_create(
            phone_number=str(row['Phone Number']),
            defaults={
                'first_name': row['First Name'],
                'last_name': row['Last Name'],
                'age': row['Age'],
                'monthly_salary': row['Monthly Salary'],
                'approved_limit': row['Approved Limit'],
            }
        )

    for _, row in loans.iterrows():
        cust = Customer.objects.filter(id=row['Customer ID']).first()
        if cust:
            Loan.objects.update_or_create(
                loan_id=row['Loan ID'],
                defaults={
                    'customer': cust,
                    'loan_amount': row['Loan Amount'],
                    'tenure': row['Tenure'],
                    'interest_rate': row['Interest Rate'],
                    'monthly_payment': row['Monthly payment'],
                    'emis_paid_on_time': row['EMIs paid on Time'],
                    'date_of_approval': row['Date of Approval'] if not pd.isnull(row['Date of Approval']) else datetime.today(),
                    'end_date': row['End Date'] if not pd.isnull(row['End Date']) else datetime.today(),
                }
            )
