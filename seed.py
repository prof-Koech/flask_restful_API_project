from app import app, db, User
from faker import Faker

# Create an instance of the Faker generator
fake = Faker()

# Create 20 users using Faker
users = []
for _ in range(20):
    user = User(
        username=fake.name(),
        email=fake.email(),
        password_hash=fake.password(),
    )
    users.append(user)

# Create application context
with app.app_context():
    # Add the users to the database session
    db.session.add_all(users)

    # Commit the changes
    db.session.commit()