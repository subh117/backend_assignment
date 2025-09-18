FROM python:3.10-slim

# Set working directory inside the app folder
WORKDIR /code/credit_approval_system

# Copy the entire project folder
COPY credit_approval_system /code/credit_approval_system
COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]
