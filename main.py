from fastapi import FastAPI
from routes.students_routes import students_api_router

app = FastAPI()

app.include_router(students_api_router)