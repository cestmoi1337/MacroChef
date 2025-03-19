import requests

# Your API key
API_KEY = "9MDqfP9eATC1nu95wH9aZcqDqUHo6bpl2PlHEWXy"

# Search for an ingredient (example: "apple")
query = "apple"
url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={query}&api_key={API_KEY}"

# Make the API request
response = requests.get(url)
data = response.json()

# Extract the first food item
if "foods" in data and len(data["foods"]) > 0:
    food_item = data["foods"][0]  # Get the first item
    print("\n--- Nutritional Info ---")
    print(f"Food Name: {food_item['description']}")
    print(f"Serving Size: {food_item.get('servingSize', 'N/A')} {food_item.get('servingSizeUnit', '')}")
    
    print("\n--- Macronutrients ---")
    for nutrient in food_item["foodNutrients"]:
        if nutrient["nutrientName"] in ["Energy", "Protein", "Carbohydrate, by difference", "Total Sugars", "Total lipid (fat)"]:
            print(f"{nutrient['nutrientName']}: {nutrient['value']} {nutrient['unitName']}")
else:
    print("No results found for the given ingredient.")

