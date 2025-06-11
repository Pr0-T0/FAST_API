from sqlalchemy import Column, Integer, String
from database import Base  # Import the Base class to inherit from

# Define the Books model/table
class Books(Base):
    __tablename__ = 'books'  # Name of the table in the database

    # Columns in the 'books' table:
    id = Column(Integer, primary_key=True, index=True)  # Unique ID for each book, also indexed for faster queries
    title = Column(String)      # Title of the book
    author = Column(String)     # Author of the book
    description = Column(String) # Short description of the book
    rating = Column(Integer)    # Integer rating (e.g., 1 to 5 stars)
