from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import datetime

# Define the Pydantic model for incoming POST data
# This ensures that the incoming JSON is validated automatically
class Item(BaseModel):
    name: str
    quantity: int
    price: float = 0.0

app = FastAPI(
    title="Simple API Service",
    description="A basic FastAPI service with GET and POST endpoints.",
    version="1.0.0"
)

# In-memory storage for demonstration
data_store: Dict[int, Item] = {}
next_id = 1

@app.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint to confirm the API is running.
    """
    return {
        "status": "API is up and running!",
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.post("/items/", tags=["Items"])
async def create_item(item: Item):
    """
    Accepts an Item object via POST and stores it.
    """
    global next_id
    item_id = next_id
    data_store[item_id] = item
    next_id += 1
    
    return {
        "message": "Item created successfully",
        "item_id": item_id,
        "data_received": item.model_dump()
    }

@app.get("/items/{item_id}", tags=["Items"])
async def get_item(item_id: int):
    """
    Retrieves a specific item by its ID.
    """
    if item_id in data_store:
        return {"item_id": item_id, "item": data_store[item_id]}
    
    return {"message": "Item not found"}

# Log message for successful startup (optional, but helpful)
print("FastAPI application initialized.")
