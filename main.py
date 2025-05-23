from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from typing import List, Optional
# from datetime import date as date_type, datetime
# import os
# from dotenv import load_dotenv
from appointments import (
    get_all_businesses, get_business, get_services, get_available_slots, get_appointment_by_business,
    create_appointment, get_all_clients, get_client_by_id, create_client
)

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://appointment-scheduler-ac2.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request models
class AppointmentCreate(BaseModel):
    # id: int
    business_id: int
    service_id: int
    client_id: int
    staff_id: int
    start_time: str
    end_time: str
    notes: str
    date: str

# Add this model to main.py with the other models
class ClientCreate(BaseModel):
    name: str
    email: str
    phone: str
    notes: str = None

# Routes
@app.get("/")
def read_root():
    return {"message": "Appointment Scheduler API"}

@app.get("/businesses")
def read_all_businesses():
    return get_all_businesses()

@app.get("/businesses/{business_id}")
def read_business(business_id: int):
    """
    The full route: https://127.0.0.1:8000/business/1
    > Google, download POSTMan (Windows), follow the installation instruction
    :param business_id:
    :return:
    """
    business = get_business(business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business

@app.get("/businesses/{business_id}/services")
def read_services(business_id: int):
    return get_services(business_id)

@app.get("/services/{service_id}/slots")
def read_available_slots(service_id: int, date: str):
    # print(service_id)
    # print(date)
    return {"slots": get_available_slots(service_id, date)}

@app.post("/appointments")
def create_new_appointment(appointment: AppointmentCreate):
    result = create_appointment(
        appointment.service_id,
        appointment.client_id,
        appointment.date,
        appointment.start_time,
        # appointment.id,
        appointment.business_id,
        appointment.staff_id,
        appointment.end_time,
        appointment.notes
    )
    if not result:
        raise HTTPException(status_code=400, detail="Could not create appointment")
    return result

@app.get("/appointments/{business_id}")
def read_appointments(business_id: int):
    return get_appointment_by_business(business_id)

@app.get("/clients")
def read_all_clients():
    """
    Get all clients
    :return:
    """
    return get_all_clients()

@app.get("/clients/{client_id}")
def read_client(client_id: int):
    """
    Get client by ID
    :param client_id:
    :return:
    """
    client = get_client_by_id(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

# Add this endpoint to main.py
@app.post("/clients")
def create_new_client(client: ClientCreate):
    """Create a new client"""
    result = create_client(
        client.name,
        client.email,
        client.phone,
        client.notes
    )
    if not result:
        raise HTTPException(status_code=400, detail="Could not create client")
    return result
# Run with: uvicorn main:app --reload