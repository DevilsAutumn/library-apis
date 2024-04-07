from fastapi import FastAPI
from app.router.urls import api_router
from config import settings
from contextlib import asynccontextmanager
from app.db.connection import Database


# Cache and persist the connection to avoid connecting on
# every DB call
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the model
    print("loading databases")
    client_instance = Database()
    client_instance.load_collection()
    yield
    # Clean up the models and release the resources
    client_instance.client.close()
    print("Database connection close")


app = FastAPI(
    docs_url="/docs" if settings.DEBUG else None,
    lifespan=lifespan
)

# add the student router/urls
app.include_router(api_router, prefix=settings.API_VERSION_STR)
