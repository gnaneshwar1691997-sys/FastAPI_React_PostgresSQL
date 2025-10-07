# Import required SQLAlchemy components
from sqlalchemy import Column, Integer, String, Float  # Data types and column definitions
from sqlalchemy.ext.declarative import declarative_base  # Base class for all ORM models

# Create a Base class — all models must inherit from this
# It helps SQLAlchemy know which classes represent database tables
Base = declarative_base()

# Define the Product table model
class Product(Base):
    # Name of the table in the database
    __tablename__ = "products"

    # Define table columns (fields)
    # Primary key column, unique for each product
    id = Column(Integer, primary_key=True, index=True)
    
    # Name of the product
    name = Column(String, index=True)
    
    # Description of the product
    description = Column(String)
    
    # Price of the product (float number)
    price = Column(Float)
    
    # Quantity available in stock (integer)
    quantity = Column(Integer)
