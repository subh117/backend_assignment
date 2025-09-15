from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import import_customers_and_loans
from .models import Customer
from rest_framework import status
import datetime
from .models import Loan, Customer

# Create your views here.

@api_view(['POST'])
def import_data(request):
    import_customers_and_loans.delay()
    return Response({'status': 'Import started'})

@api_view(['POST'])
def register(request):
    data = request.data
    salary = int(data.get('monthly_income'))
    # round approved_limit to nearest lakh
    limit = int(round(36 * salary, -5))
    customer = Customer.objects.create(
        first_name=data['first_name'],
        last_name=data['last_name'],
        age=data['age'],
        phone_number=data['phone_number'],
        monthly_salary=salary,
        approved_limit=limit,
    )
    response = {
        'customer_id': customer.id,
        'name': f"{customer.first_name} {customer.last_name}",
        'age': customer.age,
        'monthly_income': customer.monthly_salary,
        'approved_limit': customer.approved_limit,
        'phone_number': customer.phone_number,
    }
    return Response(response, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def check_eligibility(request):
    customer_id = request.data['customer_id']
    amount = float(request.data['loan_amount'])
    rate = float(request.data['interest_rate'])
    tenure = int(request.data['tenure'])
    customer = Customer.objects.get(id=customer_id)
    # Compute current loans, credit score, slabs etc (long logic)
    # See assignment for scoring!
    # Use the EMI formula below to compute monthly_installment

    def emi(P, r, n):
        monthly_rate = r/(12*100)
        return P * monthly_rate * (1+monthly_rate)**n / ((1+monthly_rate)**n-1) \
            if monthly_rate else P / n

    # Pseudo code for slabs
    # credit_rating = <your calculation>
    # if credit_rating > 50: approve
    # elif ...
    # else: reject, etc

    # return JSON per assignment
@api_view(['POST'])
def create_loan(request):
    data = request.data
    customer = Customer.objects.get(id=data['customer_id'])
    loan = Loan.objects.create(
        customer=customer,
        loan_amount=data['loan_amount'],
        tenure=data['tenure'],
        interest_rate=data['interest_rate'],
        monthly_payment=data['monthly_payment'],
        emis_paid_on_time=data.get('emis_paid_on_time', 0),
        date_of_approval=data.get('date_of_approval', datetime.date.today()),
        end_date=data.get('end_date', datetime.date.today()),
    )
    response = {
        'loan_id': loan.loan_id,
        'customer_id': loan.customer.id,
        'loan_amount': loan.loan_amount,
        'tenure': loan.tenure,
        'interest_rate': loan.interest_rate,
        'monthly_payment': loan.monthly_payment,
        'emis_paid_on_time': loan.emis_paid_on_time,
        'date_of_approval': str(loan.date_of_approval),
        'end_date': str(loan.end_date),
    }
    return Response(response, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def view_loan(request, loan_id):
    try:
        loan = Loan.objects.get(loan_id=loan_id)
        response = {
            'loan_id': loan.loan_id,
            'customer_id': loan.customer.id,
            'loan_amount': loan.loan_amount,
            'tenure': loan.tenure,
            'interest_rate': loan.interest_rate,
            'monthly_payment': loan.monthly_payment,
            'emis_paid_on_time': loan.emis_paid_on_time,
            'date_of_approval': str(loan.date_of_approval),
            'end_date': str(loan.end_date),
        }
        return Response(response)
    except Loan.DoesNotExist:
        return Response({'error': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def view_loans(request, customer_id):
    loans = Loan.objects.filter(customer__id=customer_id)
    response = [
        {
            'loan_id': loan.loan_id,
            'loan_amount': loan.loan_amount,
            'tenure': loan.tenure,
            'interest_rate': loan.interest_rate,
            'monthly_payment': loan.monthly_payment,
            'emis_paid_on_time': loan.emis_paid_on_time,
            'date_of_approval': str(loan.date_of_approval),
            'end_date': str(loan.end_date),
        }
        for loan in loans
    ]
    return Response(response)
