from database import localsesh
from models.users import Users
from models.categories import Categories
from models.transactions import Transactions
from datetime import date
from decimal import Decimal

# Open a database session
db = localsesh()

try:
    # Create a user
    alex = Users(
        username="relationship_test_alex5",
        hashed_password="test_password_hash"
    )

    # Create a category belonging to Alex
    food = Categories(
        category_name="Test Food",
        user=alex
    )

    # Create a transaction belonging to Alex and Food
    meal = Transactions(
        amount=Decimal("25.50"),
        type="expense",
        description="Test meal",
        date=date.today(),
        user=alex,
        category=food
    )

    # Save all three objects
    db.add(alex)
    db.add(food)
    db.add(meal)
    db.commit()

    # Reload the objects from the database
    db.refresh(alex)
    db.refresh(food)
    db.refresh(meal)

    # Test the relationships
    print("Alex's categories:", [c.category_name for c in alex.category])
    print("Food's owner:", food.user.username)
    print("Meal's owner:", meal.user.username)
    print("Meal's category:", meal.category.category_name)
    print("Food's transactions:", [t.description for t in food.transaction])

finally:
    db.close()