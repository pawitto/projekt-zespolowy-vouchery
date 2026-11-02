from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.db import DbSession
from app.errors import DomainError
from app.routers import customer

app = FastAPI(
    title="VoucherHub API",
    version="0.1.0",
    description="Backend systemu sprzedaży i realizacji voucherów.",
)

app.include_router(customer.router)


@app.exception_handler(DomainError)
def handle_domain_error(request: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message, "code": exc.code})


@app.get("/health", tags=["system"])
def health(db: DbSession) -> dict[str, str]:
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "ok"}
