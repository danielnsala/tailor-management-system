from fastapi import FastAPI
from app.routers.customers import router as customers_router
from app.routers.measurements import router as measurements_router
from app.routers.orders import router as orders_router
from app.routers.payments import router as payments_router
from app.routers.jobs import router as jobs_router
from app.routers.gallery import router as gallery_router

app = FastAPI(
    title="Tailor Management System",
    description="A backend API for managing customers, orders, tailoring jobs, payments, measurements, and gallery items in a tailor management system.",
    version="1.0.0",
)
app.include_router(customers_router)
app.include_router(measurements_router)
app.include_router(orders_router)
app.include_router(payments_router)
app.include_router(jobs_router)
app.include_router(gallery_router)