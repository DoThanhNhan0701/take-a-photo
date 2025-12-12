from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.models.location import Location
import sys

def assign_location_to_user(username: str):
    db: Session = SessionLocal()
    try:
        # Get User
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print(f"User '{username}' not found.")
            return

        # Get a Location (first one available)
        location = db.query(Location).first()
        
        # If no location exists, create one
        if not location:
            print("No location found. Creating a default location.")
            location = Location(
                name="Default Store",
                code="DEFAULT001",
                address="123 Default St",
                gps_latitude=10.762622,
                gps_longitude=106.660172
            )
            db.add(location)
            db.commit()
            db.refresh(location)
            print(f"Created location: {location.name} ({location.id})")
        else:
            print(f"Found location: {location.name} ({location.id})")

        # Update User
        user.location_id = location.id
        db.commit()
        db.refresh(user)
        print(f"Successfully assigned location '{location.name}' to user '{user.username}'.")
        print(f"User Location ID: {user.location_id}")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    assign_location_to_user("nhandt")
