from appointments import get_business, get_services, get_available_slots

# Test getting a business
business = get_business(1)  # Use an actual ID from your database
print(f"Business: {business['name']}")

# Test getting services
services = get_services(1)  # Use an actual business ID
for service in services:
    print(f"Service: {service['name']} - ${service['price']}")

# Test getting available slots
slots = get_available_slots(1, "2025-03-18")  # Use actual service ID and date
print(f"Available slots: {slots}")