from pydantic import BaseModel, ValidationError

# Define a simple model
class User(BaseModel):
    id: int
    name: str
    email: str
    age: int | None = None  # Optional field with default None

# Valid data
user_data = {"id": 1, "name": "Duaa", "email": "pirzadaduaa87@gmail.com", "age": 24}
user = User(**user_data)
print(user)  # id=1 name='Duaa' email='pirzadaduaa87@gmail.com' age=24
print(user.model_dump())  # {'id': 1, 'name': 'Duaa', 'email': 'pirzadaduaa87@gmail.com', 'age': 24}

# Invalid data (will raise an error)
try:
    invalid_user = User(id="not_an_int", name="dua", email="duaa_pirzada@yahoo.com")
except ValidationError as e:
    print(e)