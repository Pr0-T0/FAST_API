# Import necessary SQLAlchemy components
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define the database URL
# For SQLite, the format is: "sqlite:///./<filename>.db"
# "./books.db" creates the DB file in the current directory
SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"

# Create the SQLAlchemy engine
# connect_args={"check_same_thread": False} is required for SQLite
# to allow usage of the same connection in different threads (used in FastAPI)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Create a configured "SessionLocal" class
# Each instance of SessionLocal will be a new database session
SessionLocal = sessionmaker(
    autocommit=False,  # Disable auto commit - you'll need to commit manually
    autoflush=False,   # Disable auto flush - changes aren't automatically pushed to DB
    bind=engine        # Bind the session to our engine
)

# Create a base class for all our database models to inherit from
# Later, when defining models (like Book), you'll inherit from Base
Base = declarative_base()
