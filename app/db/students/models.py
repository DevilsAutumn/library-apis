from pydantic import BaseModel, Field


class Address(BaseModel):
    city: str = Field(..., description="The city where the student resides")
    country: str = Field(..., description="The country where the student resides")


class StudentBase(BaseModel):
    name: str = Field(..., description="The name of the student")
    age: int = Field(..., gt=5, description="The age of the student (must be greater than 0)")


class Student(StudentBase):
    address: Address


class StudentIdOut(BaseModel):
    id: str = Field(..., description="The unique identifier of the student")
