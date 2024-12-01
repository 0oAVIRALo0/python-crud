def student_serializer(student) -> dict:
  return {
    "id": str(student["_id"]),
    "name": student["name"],
    "age": student["age"],
    "address": student["address"],
  }