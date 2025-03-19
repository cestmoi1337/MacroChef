import firebase_admin
from firebase_admin import credentials, firestore
import requests

# ✅ Initialize Firebase Admin SDK (Replace with your Firestore credentials)
cred = credentials.Certificate("path/to/your/firebase_credentials.json")  
firebase_admin.initialize_app(cred)

# ✅ Firestore Database Instance
db = firestore.client()

# ✅ Your USDA API Key
API_KEY = "9MDqfP9eATC1nu95wH9aZcqDqUHo6bpl2PlHEWXy"

def fetch_nutrition_data(food_query):
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_query}&api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def store_food_data(food_query):
    data = fetch_nutrition_data(food_query)
    if not data or "foods" not in data:
        print("No data found!")
        return
    
    for food in data["foods"]:
        food_id = food.get("fdcId")
        food_name = food.get("description", "Unknown Food")
        
        # ✅ Extract Key Nutrition Data
        nutrients = {}
        for nutrient in food.get("foodNutrients", []):
            nutrients[nutrient["nutrientName"]] = nutrient["value"]
        
        # ✅ Prepare Firestore Data Structure
        food_data = {
            "fdcId": food_id,
            "name": food_name,
            "brandOwner": food.get("brandOwner", "Unknown"),
            "category": food.get("foodCategory", "Uncategorized"),
            "servingSize": food.get("servingSize", 100),
            "servingUnit": food.get("servingSizeUnit", "g"),
            "nutrients": nutrients
        }

        # ✅ Store Data in Firestore
        db.collection("food_nutrition").document(str(food_id)).set(food_data)
        print(f"✅ Stored {food_name} in Firestore!")

# 🔥 Example: Store Apple Nutrition Data in Firestore
store_food_data("apple")

