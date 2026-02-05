from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.database import engine
from modules.trips import trip_schema, trip_routes
from modules.schools import school_schema, school_routes
from modules.parents import parent_schema, parent_routes
from modules.students import student_schema, student_routes
from modules.booking import booking_schema, booking_routes
from modules.payments import payment_routes, payment_schema
from modules.schools.school_seeder import seed_data as seed_school_data
from modules.parents.parent_seeder import seed_data as seed_parent_data
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from middlewares.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
    generic_exception_handler,
)

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:3000",
]
# This will create all the tables defined by your models
school_schema.Base.metadata.create_all(bind=engine)
trip_schema.Base.metadata.create_all(bind=engine)
parent_schema.Base.metadata.create_all(bind=engine)
student_schema.Base.metadata.create_all(bind=engine)
booking_schema.Base.metadata.create_all(bind=engine)
payment_schema.Base.metadata.create_all(bind=engine)



@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    seed_school_data()
    seed_parent_data()
    yield
    # on shutdown

app = FastAPI(lifespan=lifespan)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
# Note: It's good practice to keep the generic exception handler last
app.add_exception_handler(Exception, generic_exception_handler)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include the all the routers here
app.include_router(trip_routes.router)
app.include_router(school_routes.router)
app.include_router(parent_routes.router)
app.include_router(student_routes.router)
app.include_router(booking_routes.router)
app.include_router(payment_routes.router)


# this is for health check
@app.get("/")
async def root():
    return {"message": "Hello World"}