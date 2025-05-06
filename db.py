import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

def test_connection():
    """Test the Supabase connection"""
    try:
        # Try a simple query
        response = supabase.table("businesses").select("*").limit(1).execute()
        print("Connection successful!")
        print(f"Response: {response}")
        return True
    except Exception as e:
        print(f"Connection error: {e}")
        return False

if __name__ == "__main__":
    test_connection()
