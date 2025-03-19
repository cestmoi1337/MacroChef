import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("firebase_credentials.json")  # Ensure this path is correct
firebase_admin.initialize_app(cred)
db = firestore.client()

# Fetch all documents in 'usda_foods' collection
docs = db.collection("usda_foods").stream()

# Count documents
count = sum(1 for _ in docs)
print(f"Total USDA Foods in Firestore: {count}")
