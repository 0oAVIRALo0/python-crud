from pydantic import BaseModel
from typing import Optional

class Address(BaseModel):
    city: str
    country: str

class Student(BaseModel):
    name: str
    age: int
    address: Address

    class Config:
        orm_mode = True

class StudentOptional(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[Address] = None