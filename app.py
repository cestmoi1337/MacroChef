from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase if not already initialized
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("/Users/grevolorio/Development/Projects/firebase_credentials.json")  # Adjust path if needed
    firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    search_query = ""
    nutrient_filter = ""

    if request.method == "POST":
        search_query = request.form.get("search_query", "").strip().lower()
        nutrient_filter = request.form.get("nutrient_filter", "").strip().lower()

        # Fetch all food documents
        food_docs = db.collection("usda_foods").stream()

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
                        results.append({"description": description, "category": category, "nutrients": matching_nutrients})
                else:
                    results.append({"description": description, "category": category, "nutrients": nutrients})

    return render_template("index.html", results=results, search_query=search_query, nutrient_filter=nutrient_filter)

if __name__ == "__main__":
    app.run(debug=True)
