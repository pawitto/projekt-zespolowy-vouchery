from fastapi import FastAPI
from sqlalchemy import text

from app.db import DbSession

app = FastAPI(
    title="VoucherHub API",
    version="0.1.0",
    description="Backend systemu sprzedaży i realizacji voucherów.",
)


@app.get("/health", tags=["system"])
def health(db: DbSession) -> dict[str, str]:
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "ok"}
