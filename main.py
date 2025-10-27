# Importing necessary libraries and modules
from fastapi import FastAPI, Depends, HTTPException  # FastAPI core, dependency injection, and HTTP error handling
from fastapi.middleware.cors import CORSMiddleware  # Middleware to handle Cross-Origin Resource Sharing (CORS)
from sqlalchemy.orm import Session  # SQLAlchemy Session for database interaction
import database_models  # Import your SQLAlchemy models (tables)
from database import SessionLocal, engine  # Database session creation and engine connection
from models import Product  # Pydantic model for input/output validation
# Create all tables in the database if they don't exist already
database_models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Configure CORS middleware so frontend React app can access API without issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow only the local React dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Dependency function to get a database session for each request.
def get_db():
    db = SessionLocal()  # Create a new database session
    try:
        yield db  # Provide session to the request
    finally:
        db.close()  # Ensure the session is closed after request completes

# Sample list of products for initializing the database
products = [
    Product(id=1, name="Phone", description="A smartphone", price=699.99, quantity=50),
    Product(id=2, name="Laptop", description="A powerful laptop", price=999.99, quantity=30),
    Product(id=3, name="Pen", description="A blue ink pen", price=1.99, quantity=100),
    Product(id=4, name="Table", description="A wooden table", price=199.99, quantity=20),
]

# Another single product example (not used in init)
product = Product(id=5, name="Chair", description="A comfortable chair", price=89.99, quantity=15)

# Function to initialize database with sample products if empty
def init_db():
    db = SessionLocal()  # Open a new database session

    # Check if database already has products
    existing_count = db.query(database_models.Product).count()

    # If database is empty, add the sample products
    if existing_count == 0:
        for product in products:
            # Convert Pydantic model to SQLAlchemy model using **kwargs
            db.add(database_models.Product(**product.model_dump()))
        db.commit()  # Save changes to the database
        print("Database initialized with sample products.")
        
    db.close()  # Close session

# Call the init_db function at startup
init_db()    

# --------------------- API Endpoints ---------------------

# GET all products
@app.get("/products/")
def get_all_products(db: Session = Depends(get_db)):  # Inject DB session using Depends
    products = db.query(database_models.Product).all()  # Query all products from database
    return products  # Return list of products

# GET a product by its ID
@app.get("/products/{product_id}")
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    # Query the database for a product with the specified ID
    product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if product:
        return product  # Return product if found
    return {"error": "Product not found"}  # Return error if not found

# POST a new product
@app.post("/products/")
def create_product(product: Product, db: Session = Depends(get_db)):
    # Add new product to database (convert Pydantic model to SQLAlchemy model)
    db.add(database_models.Product(**product.model_dump()))
    db.commit()  # Save changes
    return {"message": "Product created successfully", "product": product}  # Return success message

# PUT/Update an existing product by ID
@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product, db: Session = Depends(get_db)):
    # Find product in database
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")  # Raise 404 if not found
    
    # Update product fields
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity
    
    db.commit()  # Save changes
    db.refresh(db_product)  # Refresh to get updated data
    return {"message": "Product updated successfully", "product": db_product}

# DELETE a product by ID
@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    # Find product in database
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")  # Raise 404 if not found
    
    db.delete(db_product)  # Delete product
    db.commit()  # Save changes
    return {"message": "Product deleted successfully"}
