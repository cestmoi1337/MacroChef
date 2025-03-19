import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase if not already initialized
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("/Users/grevolorio/Development/Projects/firebase_credentials.json")  # Adjust path if needed
    firebase_admin.initialize_app(cred)

db = firestore.client()

def search_food():
    search_query = input("\nEnter a food name or category to search: ").strip().lower()
    nutrient_filter = input("Enter a nutrient name to filter by (or press Enter to skip): ").strip().lower()

    print("\n🔎 Searching Firestore...\n")
    
    # Fetch all food documents
    food_docs = db.collection("usda_foods").stream()

    results = []
    
    for doc in food_docs:
        food_data = doc.to_dict()
        description = food_data.get("description", "No Description")
        category = food_data.get("foodCategory", "Unknown Category")
        nutrients = food_data.get("foodNutrients", [])

        # Check if search query matches food name or category
        if search_query in description.lower() or search_query in category.lower():
            if nutrient_filter:
                # Filter results by nutrient name
                matching_nutrients = [n for n in nutrients if nutrient_filter in n.get("nutrientName", "").lower()]
                if matching_nutrients:
                    results.append((description, category, matching_nutrients))
            else:
                results.append((description, category, nutrients))

    if results:
        print("🔎 Search Results:")
        for i, (desc, cat, nutrients) in enumerate(results, start=1):
            print(f"{i}. {desc} - Category: {cat}")
            if nutrients:
                print("   Nutrients:")
                for nutrient in nutrients:
                    print(f"   - {nutrient['nutrientName']}: {nutrient['value']} {nutrient['unitName']}")
            print("-" * 50)
    else:
        print("❌ No matching results found.")

def list_all_foods():
    print("\n📜 Fetching all foods from Firestore...\n")
    food_docs = db.collection("usda_foods").stream()
    count = 0
    for doc in food_docs:
        food_data = doc.to_dict()
        print(f"🔹 {food_data.get('description', 'No Description')} - Category: {food_data.get('foodCategory', 'Unknown')}")
        count += 1
    print(f"\n✅ Total foods: {count}")

def main_menu():
    while True:
        print("\n📌 USDA Food Database CLI")
        print("1️⃣ Search for food")
        print("2️⃣ List all foods")
        print("3️⃣ Exit")
        
        choice = input("\nEnter your choice (1/2/3): ").strip()

        if choice == "1":
            search_food()
        elif choice == "2":
            list_all_foods()
        elif choice == "3":
            print("👋 Exiting program. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()
