from fastapi import APIRouter, Query, HTTPException, Path
from config.database import collection_name
from models.students_model import Student, StudentOptional
from schemas.students_schemas import student_serializer
from bson import ObjectId

students_api_router = APIRouter()

# POST: Create Student
@students_api_router.post("/students", status_code=201, summary="Create Students", description="API to create a student in the system. All fields are mandatory and required while creating the student in the system.")
async def create_student(student: Student):
	try:
		student_dict = student.model_dump()
		result = collection_name.insert_one(student_dict)
		return {"id": str(result.inserted_id)}
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error inserting student: {str(e)}")

# GET: List Students with filters
@students_api_router.get("/students", status_code=200, summary="List students", description="An API to find a list of students. You can apply filters on this API by passing the query parameters as listed below.")
async def list_students(country: str = Query(None, description="To apply filter of country. If not given or empty, this filter should be applied."), age: int = Query(None, description="Only records which have age greater than equal to the provided age should be present in the result. If not given or empty, this filter should be applied.")):
	try:
		query = {}
		if country:
			query["address.country"] = country
		if age:
			query["age"] = {"$gte": age}
		
		students = collection_name.find(query)
		result = [student_serializer(student) for student in students]
		response = {"data": []}
		
		for student in result:
			student_info = {
				"name": student["name"],
				"age": student["age"]
			}
			response["data"].append(student_info)

		return response

	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error fetching students: {str(e)}")


# GET: Fetch Student by ID
@students_api_router.get("/students/{id}", status_code=200, summary="Fetch student")
async def fetch_student(id: str = Path(..., description="The ID of the student previously created.")):
	try:
		student = collection_name.find_one({"_id": ObjectId(id)})
		if not student:
			raise HTTPException(status_code=404, detail="Student not found")
		
		result = student_serializer(student)
		response = {
			"name": result["name"],
			"age": result["age"],
			"address": result["address"]
		}

		return response
	
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error fetching student: {str(e)}")
	
# PATCH: Update Student by ID
@students_api_router.patch("/students/{id}", status_code=204, summary="Update student", description="API to update the student's properties based on information provided. Not mandatory that all information would be sent in PATCH, only what fields are sent should be updated in the Database.")
async def update_student(id: str, updated_data: StudentOptional):
	try:
		update_body = updated_data.model_dump(exclude_unset=True)
		
		if not update_body:
			raise HTTPException(status_code=400, detail="No data to update")
		
		result = collection_name.update_one({"_id": ObjectId(id)}, {"$set": update_body})
		
		if result.matched_count == 0:
			raise HTTPException(status_code=404, detail="Student not found")
		
		return {}

	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error updating student: {str(e)}")

# DELETE: Delete Student
@students_api_router.delete("/students/{id}", status_code=200, summary="Delete student")
async def delete_student(id: str):
	try:
		result = collection_name.delete_one({"_id": ObjectId(id)})
		if result.deleted_count == 0:
			raise HTTPException(status_code=404, detail="Student not found")
		return {}
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error deleting student: {str(e)}")
