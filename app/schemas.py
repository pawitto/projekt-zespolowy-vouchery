from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, EmailStr


class ORMModel(BaseModel):
    """Bazowa klasa DTO: pozwala budować DTO wprost z encji SQLAlchemy."""

    model_config = ConfigDict(from_attributes=True)


class PartnerPublic(ORMModel):
    id: int
    name: str


class OfferOut(ORMModel):
    id: int
    name: str
    description: str
    price: Decimal
    validity_days: int
    partner: PartnerPublic


class PurchaseRequest(BaseModel):
    email: EmailStr


class VoucherDisplayStatus(StrEnum):
    ACTIVE = "ACTIVE"
    USED = "USED"
    EXPIRED = "EXPIRED"


class VoucherOut(BaseModel):
    code: str
    status: VoucherDisplayStatus
    price_paid: Decimal
    purchased_at: datetime
    expires_at: datetime
    redeemed_at: datetime | None
    offer: OfferOut
