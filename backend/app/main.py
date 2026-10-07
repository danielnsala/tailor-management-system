from fastapi import FastAPI
from app.routers.customers import router as customers_router

app = FastAPI(
    title="Tailor Management System",
    description="A backend API for managing customers, orders, tailoring jobs, payments, measurements, and gallery items in a tailor management system.",
    version="1.0.0",
)
app.include_router(customers_router)