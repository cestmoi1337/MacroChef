import firebase_admin
from firebase_admin import credentials, firestore
import requests

# Initialize Firebase Admin SDK
cred = credentials.Certificate("firebase_credentials.json")  # Path to your Firebase JSON file
firebase_admin.initialize_app(cred)

# Get a Firestore database instance
db = firestore.client()

# USDA API Key
USDA_API_KEY = "9MDqfP9eATC1nu95wH9aZcqDqUHo6bpl2PlHEWXy"

# Function to fetch data from USDA API
def fetch_usda_data(query, page_size=50):
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={USDA_API_KEY}&query={query}&pageSize={page_size}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("❌ Failed to fetch data:", response.status_code, response.text)
        return None

# Function to save data to Firestore
def save_to_firestore(data):
    if "foods" in data:
        for food in data["foods"]:
            food_id = str(food["fdcId"])  # Use USDA Food ID as document ID
            db.collection("usda_foods").document(food_id).set(food)
        print("✅ Data successfully saved to Firestore!")
    else:
        print("❌ No food data found.")

# Example: Fetch and store apple data
food_data = fetch_usda_data("apple")
if food_data:
    save_to_firestore(food_data)
