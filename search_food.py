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
    results_per_page = int(input("How many results per page? (default 5): ") or 5)

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

    if not results:
        print("❌ No matching results found.")
        return

    # Implement pagination
    total_results = len(results)
    current_page = 0

    while True:
        start = current_page * results_per_page
        end = start + results_per_page
        paginated_results = results[start:end]

        print(f"\n🔎 Page {current_page + 1}/{(total_results // results_per_page) + 1} 🔎")
        for i, (desc, cat, nutrients) in enumerate(paginated_results, start=start + 1):
            print(f"{i}. {desc} - Category: {cat}")
            if nutrients:
                print("   Nutrients:")
                for nutrient in nutrients:
                    print(f"   - {nutrient['nutrientName']}: {nutrient['value']} {nutrient['unitName']}")
            print("-" * 50)

        # Pagination options
        print("\nCommands: [n] Next | [p] Previous | [q] Quit")
        command = input("Enter command: ").strip().lower()

        if command == "n" and end < total_results:
            current_page += 1
        elif command == "p" and current_page > 0:
            current_page -= 1
        elif command == "q":
            print("✅ Exiting search.")
            break
        else:
            print("⚠️ Invalid command or no more pages.")

if __name__ == "__main__":
    search_food()
