import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

def get_business(business_id):
    """Get a business by ID"""
    response = (supabase.table("businesses")
                .select("*")
                .eq("id", business_id)
                .execute())
    print(response.data)
    return response.data[0] if response.data else None

def get_all_businesses():
    """Get all businesses"""
    response = (supabase.table("businesses")
                .select("*")
                .execute())
    print(response.data)
    return response.data if response.data else None

def get_all_clients():
    """Get all clients"""
    response = (supabase.table("clients")
                .select("*")
                .execute())
    print(response.data)
    return response.data if response.data else None

def get_client_by_id(client_id):
    """Get a client by ID"""
    response = (supabase.table("clients")
                .select("*")
                .eq("id", client_id)
                .execute())
    print(response.data)
    return response.data[0] if response.data else None

def get_services(business_id):
    """Get all services for a specific business"""
    response = (supabase.table("services")
                .select("*")
                .eq("business_id", business_id)
                .execute())
    print(response.data)
    return response.data if response.data else None

def get_appointment_by_business(business_id):
    """Get all appointments for a business"""
    response = (supabase.table("appointments")
                .select("*")
                .eq("business_id", business_id)
                .execute())
    print(response.data)
    return response.data if response.data else None

def get_available_slots(service_id, date):
    """Get available timeslots for a service on a specific date"""
    # First, get the service to know its duration
    service_response = (supabase.table("services")
                        .select("*,businesses(*)")
                        # .select("*,businesses_hours(*)")
                        .eq("id", service_id).execute())

    if not service_response.data:
        return []

    service = service_response.data[0]
    business = service["businesses"]
    duration = service["duration"]

    # Check if the business is open on that date
    # Get business hours for the specific day
    day_of_week = datetime.strptime(date, "%Y-%m-%d").strftime("%A").lower()
    hours_str = business["business_hours"][day_of_week]

    if hours_str == "closed":
        return []

    # Parse hours
    start_time, end_time = hours_str.split("-")
    start_hour, start_minute = map(int, start_time.split(":"))
    end_hour, end_minute = map(int, end_time.split(":"))

    # Create time slots
    slots = []
    current = datetime.strptime(f"{date} {start_hour}:{start_minute}", "%Y-%m-%d %H:%M")
    end = datetime.strptime(f"{date} {end_hour}:{end_minute}", "%Y-%m-%d %H:%M")

    while current + timedelta(minutes=int(duration)) <= end:
        slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=int(duration))

    
    # Get booked appointments for that day
    appointments_response = (supabase.table("appointments")
                             .select("start_time")
                             .eq("service_id", service_id)
                             .eq("date", date).execute())
    booked_times = [appointment["start_time"] for appointment in appointments_response.data]

    # # Filter out booked slots
    available_slots = [slot for slot in slots if slot not in booked_times]

    return available_slots

def create_appointment(service_id, client_id, date, start_time, business_id, staff_id, end_time, notes):
    """Create a new appointment"""
    appointment_data = {
        # "id": id,
        "business_id": business_id,
        "service_id": service_id,
        "client_id": client_id,
        "staff_id": staff_id,
        "start_time": start_time,
        "end_time": end_time,
        "status": "scheduled",
        "notes": notes,
        "date": date
    }

    print(appointment_data)
    response = supabase.table("appointments").insert(appointment_data).execute()
    return response.data[0] if response.data else None

# Add more functions as needed