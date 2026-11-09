from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, EmailStr, Field


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


class LoginRequest(BaseModel):
    login: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=200)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime


class PartnerMe(ORMModel):
    id: int
    name: str
    login: str


class PartnerOfferOut(ORMModel):
    """Oferta widziana przez partnera: z polem active i datą utworzenia."""

    id: int
    name: str
    description: str
    price: Decimal
    validity_days: int
    active: bool
    created_at: datetime


class OfferCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=5000)
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    validity_days: int = Field(gt=0, le=3650)


class OfferStatusUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")  # reguła 10: zmieniamy tylko status

    active: bool


class VoucherOfferInfo(ORMModel):
    """Na co jest voucher: to widzi recepcja po wpisaniu kodu."""

    id: int
    name: str
    description: str


class PartnerVoucherOut(BaseModel):
    code: str
    status: VoucherDisplayStatus
    price_paid: Decimal
    purchased_at: datetime
    expires_at: datetime
    redeemed_at: datetime | None
    offer: VoucherOfferInfo
