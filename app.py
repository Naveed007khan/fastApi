from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# 1. Initialize the FastAPI app
app = FastAPI(
    title="Simple In-Memory API",
    description="A basic FastAPI example using GET and POST, no database.",
    version="1.0.0"
)

# --- In-Memory Storage ---
# This list will hold our 'items' data. 
# The data is lost when the server is restarted.
fake_item_db = []

# --- Pydantic Data Models ---
# Define the structure for an incoming item (used for POST request body)
class ItemIn(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

# Define the structure for an item to be returned (used for GET response)
class ItemOut(ItemIn):
    item_id: int

# --- API Endpoints ---

## 🚀 GET Endpoint: Read All Items

@app.get("/items", response_model=List[ItemOut], tags=["Items"])
async def read_items():
    """
    Retrieves all items stored in the in-memory list.
    """
    return fake_item_db

## 📝 POST Endpoint: Create an Item

@app.post("/items", response_model=ItemOut, status_code=201, tags=["Items"])
async def create_item(item: ItemIn):
    """
    Adds a new item to the in-memory list.
    
    - The item is assigned a unique, sequential ID.
    """
    # 1. Generate a simple ID (simulating a DB primary key)
    # The ID is the current length of the list + 1
    new_id = len(fake_item_db) + 1
    
    # 2. Create the complete item dictionary (including the ID)
    new_item = item.model_dump() # Converts Pydantic model to dict
    new_item["item_id"] = new_id
    
    # 3. Store the new item in the in-memory list
    fake_item_db.append(new_item)
    
    # 4. Return the created item
    return new_item

# --- Root Endpoint (Optional) ---

@app.get("/", tags=["Root"])
async def root():
    """
    A simple welcome message at the root URL.
    """
    return {"message": "Welcome to the Simple FastAPI App! Go to /docs for API details."}

