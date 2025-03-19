import firebase_admin
from firebase_admin import credentials, firestore
import os

# Set the absolute path to your credentials file
CREDENTIALS_PATH = "/Users/grevolorio/Development/Projects/firebase_credentials.json"  # Replace this with the correct path

# Initialize Firebase
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate(CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()


def search_foods(search_term):
    """
    Search for food items in Firestore that match the given search term.
    :param search_term: The name or category of the food to search for.
    """
    search_term = search_term.lower()
    results = []

    # Query Firestore
    foods_ref = db.collection("usda_foods")
    docs = foods_ref.stream()

    for doc in docs:
        food_data = doc.to_dict()
        description = food_data.get("description", "").lower()
        category = food_data.get("foodCategory", "").lower()

        # Check if the search term is in the description or category
        if search_term in description or search_term in category:
            results.append(food_data)

    return results

if __name__ == "__main__":
    search_query = input("Enter a food name or category to search: ")
    matching_foods = search_foods(search_query)

    if matching_foods:
        print("\n🔎 Search Results:")
        for idx, food in enumerate(matching_foods, start=1):
            print(f"{idx}. {food['description']} - Category: {food.get('foodCategory', 'Unknown')}")
    else:
        print("\n❌ No matching foods found.")
