import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Sample data for businesses
businesses = [
    {
        "name": "Stylish Cuts Barbershop",
        "email": "info@stylishcuts.example",
        "phone": "555-123-4567",
        "address": "123 Main St, Boston, MA",
        "business_hours": {
            "monday": "9:00-17:00",
            "tuesday": "9:00-17:00",
            "wednesday": "9:00-17:00",
            "thursday": "9:00-17:00",
            "friday": "9:00-17:00",
            "saturday": "10:00-15:00",
            "sunday": "closed"
        }
    },
    # Add 3-6 more sample businesses
]

# Sample data for services
services = [
    {
        "business_id": None,  # We'll set this after creating businesses
        "name": "Regular Haircut",
        "duration": 30,
        "price": 25.00,
        "description": "Standard haircut with clippers and scissors"
    },
    # Add more services for each business
]

# Sample data for clients
clients = [
    {
        "name": "James Smith",
        "email": "james@example.com",
        "phone": "555-987-6543",
        "notes": "Prefers afternoon appointments"
    },
    # Add 5-10 more clients
]

# Insert businesses
def seed_businesses():
    print("Seeding businesses...")
    for business in businesses:
        try:
            response = supabase.table("businesses").insert(business).execute()
            print(f"Added business: {business['name']}")
        except Exception as e:
            print(f"Error adding business {business['name']}: {e}")

# Insert services (with business IDs)
def seed_services():
    print("Seeding services...")
    # First get business IDs
    response = supabase.table("businesses").select("id, name").execute()
    business_data = response.data

    # For each business, add their services
    for business in business_data:
        # Add 3-5 services per business
        business_services = [
            {
                "business_id": business["id"],
                "name": "Regular Haircut",
                "duration": 30,
                "price": 25.00,
                "description": "Standard haircut with clippers and scissors"
            },
            {
                "business_id": business["id"],
                "name": "Beard Trim",
                "duration": 15,
                "price": 15.00,
                "description": "Professional beard shaping and trimming"
            },
            # Add more services
        ]

        for service in business_services:
            try:
                supabase.table("services").insert(service).execute()
                print(f"Added service: {service['name']} for {business['name']}")
            except Exception as e:
                print(f"Error adding service {service['name']}: {e}")

# Add similar functions for clients and a few appointments

if __name__ == "__main__":
    seed_businesses()
    seed_services()
    # Call other seeding functions
    print("Database seeding completed!")