from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date as date_type
from appointments import (
    get_business, get_services, get_available_slots, get_appointments,
    create_appointment, get_all_clients, get_client_by_id
)

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # When you push to production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request models
class AppointmentCreate(BaseModel):
    service_id: int
    client_id: int
    date: str
    start_time: str

# Routes
@app.get("/")
def read_root():
    return {"message": "Appointment Scheduler API"}

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
    return {"slots": get_available_slots(service_id, date)}

@app.post("/appointments")
def create_new_appointment(appointment: AppointmentCreate):
    result = create_appointment(
        appointment.service_id,
        appointment.client_id,
        appointment.date,
        appointment.start_time
    )
    if not result:
        raise HTTPException(status_code=400, detail="Could not create appointment")
    return result

@app.get("/appointments")
def read_appointments():
    return get_appointments()

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
# Run with: uvicorn main:app --reload