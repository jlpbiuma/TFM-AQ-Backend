from pymongo import MongoClient

# MongoDB connection string with authentication
connection_string = 'mongodb://root:password@localhost:27017/'

# Connect to MongoDB
client = MongoClient(connection_string)

# Select database
db = client['AQ']

# Select collection
collection = db['Usuario']

# Create a new document
new_document = {
    'name': 'John Doe',
    'age': 30,
    'email': 'john@example.com'
}

# Insert the document into the collection
result = collection.insert_one(new_document)

# Print the inserted document's ID
print('Inserted document ID:', result.inserted_id)
