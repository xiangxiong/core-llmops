import os
from dotenv import load_dotenv
from pymilvus import MilvusClient, DataType

load_dotenv()
# A valid token could be either
# - An API key, or 
# - A colon-joined cluster username and password, as in `user:pass`

# 1. Set up a Milvus client
client = MilvusClient(
    uri=os.getenv("CLUSTER_ENDPOINT"),
    token=os.getenv("TOKEN") 
)

# 2. Define collection name
collection_name = "example_collection"

# 3. Check if collection exists and drop it if it does (for demo purposes)
if client.has_collection(collection_name):
    client.drop_collection(collection_name)
    print(f"Dropped existing collection: {collection_name}")

# 4. Define schema and create collection
print("Creating collection...")
client.create_collection(
    collection_name=collection_name,
    dimension=1536,  # Dimension of the embedding vectors
    primary_field_name="id",
    primary_field_type=DataType.INT64,
    auto_id=True,  # Let Milvus auto-generate IDs
    vector_field_name="vector",
    metric_type="COSINE"  # Similarity metric for vector comparison
)

# 5. Verify collection creation
print(f"Collection created: {collection_name}")
print(f"Current collections: {client.list_collections()}")

# 6. Get collection information
collection_info = client.describe_collection(collection_name)
print(f"Collection information: {collection_info}")