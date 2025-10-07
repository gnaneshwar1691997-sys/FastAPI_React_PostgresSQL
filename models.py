# Import BaseModel from Pydantic
# BaseModel is used to define data models with type checking and validation
from pydantic import BaseModel


# Define a Product data model
class Product(BaseModel):
    # Product ID (integer)
    id: int
    
    # Product name (string)
    name: str
    
    # Description of the product (string)
    description: str
    
    # Price of the product (floating-point number)
    price: float
    
    # Quantity available in stock (integer)
    quantity: int
