import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase (if not already initialized)
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_credentials.json")
    firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()

# Fetch all documents from 'usda_foods'
docs = db.collection("usda_foods").limit(10).stream()

# Print the retrieved documents
print("Fetching USDA Foods from Firestore...\n")
for doc in docs:
    print(f"ID: {doc.id}")
    print(f"Data: {doc.to_dict()}\n")
