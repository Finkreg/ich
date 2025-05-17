from pydantic import BaseModel, EmailStr, Field, ValidationError, model_validator

# creating pydantic model for class Address
class Address(BaseModel):
    city: str = Field(min_length=2)
    street: str = Field(min_length=3)
    house_number: int= Field(gt=0)

# creating pydantic model for class User
class User(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(gt=0, lt=120)
    email: EmailStr
    is_employed: bool = Field(default=True)
    address: Address


    # creating validator to check if user is allowed to work
    @model_validator(mode='after')
    def validate_employment_age(self):

        if self.age is not None and self.is_employed and (self.age < 18 or self.age > 65):
            raise ValueError ("user cannot be employed because of age restrictions!")
        return self

    # str method overriding
    def __str__(self):
        return (
            f"User: {self.name},\n"
            f"age:{self.age},\n"
            f"email: {self.email},\n"
            f"city: {self.address.city,}, \n"
            f"street: {self.address.street}\n"
            f"house_number: {self.address.house_number}"
    )

# user 1 JSON
user1_json_str = """{
    "name": "Alice",
    "age": 17,
    "email": "alice@google.com",
    "is_employed": true,
    "address": {
        "city": "London",
        "street": "Baker Str.",
        "house_number": 22
    }
}"""

# user 2 JSON
user2_json_str = """{
    "name": "Homer Simpson",
    "age": 35,
    "email": "homer@donut.com",
    "is_employed": true,
    "address": {
        "city": "Springfield",
        "street": "Evergreen Terrace",
        "house_number": 742
    }
}"""

# user 3 JSON
user3_json_str = """{
    "name": "Rick Sanchez",
    "age": 60,
    "email": "multiverse-picklerick.com",
    "is_employed": false,
    "address": {
        "city": "Seattle",
        "street": "Unknown",
        "house_number": 10
    }
}"""

# function that processes the user and dumps JSON file
def check_user(data):
    try:
        user = User.model_validate_json(data)
        return user.model_dump_json()
    except ValidationError as e:
        print("Validation Error", e)
        return None

print(check_user(user1_json_str))
print(check_user(user2_json_str))
print(check_user(user3_json_str))








