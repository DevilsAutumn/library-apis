from fastapi import APIRouter, HTTPException
from app.db.students.models import Student, StudentIdOut
from app.db.connection import Database
from bson import ObjectId

router = APIRouter()
student_collection = Database().load_collection()


@router.post("", response_model=StudentIdOut, status_code=201)
async def create_student(student_post_data: Student):
    """
    Create a new student
    request body - Student
    response body - id
    """
    try:
        # Insert the student into the database
        result = await student_collection.insert_one(student_post_data.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"id": str(result.inserted_id)}


@router.get("", status_code=200)
async def list_students(country: str = None, age: int = None):
    """
    List all the students
    response body - List[Student(name, age)]
    """
    # Build filter conditions based on query parameters
    filter_conditions = {}
    if country:
        filter_conditions["address.country"] = country
    if age is not None:
        filter_conditions["age"] = {"$gte": age}

    try:
        # Include only name and age fields, exclude _id field
        projection = {"name": 1, "age": 1, "_id": 0}
        students = await student_collection.find(
            projection=projection,
            filter=filter_conditions
        ).to_list(None)
        return {"data": students}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=Student, status_code=200)
async def retrieve_student(id: str):
    """
    Retrieves a particular student
    - arg
    :id - id of a particluar student
    response body - Student
    """
    try:
        # Convert student_id string to ObjectId
        obj_id = ObjectId(id)

        # Fetch student data from MongoDB based on the provided ID
        student_data = await student_collection.find_one({"_id": obj_id})

        if student_data:
            return Student(**student_data)
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{id}", response_model=None, status_code=204)
async def update_student(id: str, student_put_data: Student):
    """
    Updates a particlular student

    - arg
    :id - id of a particlua student
    request body - Student
    response body - No content
    """
    try:
        # Convert student_id string to ObjectId
        obj_id = ObjectId(id)

        student_data = await student_collection.find_one({"_id": obj_id})

        if student_data:
            update_data = student_put_data.model_dump(exclude_unset=True)
            await student_collection.update_one(
                {"_id": obj_id},
                {"$set": update_data}
            )
            return {}
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}", status_code=200)
async def delete_student(id: str):
    """
    Deletes a particlular student

    - arg
    :id - id of a particlua student
    """
    try:
        # Convert student_id string to ObjectId
        obj_id = ObjectId(id)

        result = await student_collection.delete_one({"_id": obj_id})

        if result.deleted_count == 1:
            return {}
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
