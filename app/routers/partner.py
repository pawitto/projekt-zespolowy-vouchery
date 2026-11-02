from fastapi import APIRouter, status

from app.db import DbSession
from app.dependencies import CurrentPartner
from app.schemas import (
    LoginRequest,
    OfferCreate,
    OfferStatusUpdate,
    PartnerMe,
    PartnerOfferOut,
    TokenResponse,
)
from app.security import create_access_token
from app.services import auth as auth_service
from app.services import offers as offer_service

router = APIRouter(prefix="/api/v1/partner", tags=["partner"])


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: DbSession):
    partner = auth_service.authenticate(db, body.login, body.password)
    token, expires_at = create_access_token(partner.id)
    return TokenResponse(access_token=token, expires_at=expires_at)


@router.get("/me", response_model=PartnerMe)
def me(partner: CurrentPartner):
    return partner


@router.get("/offers", response_model=list[PartnerOfferOut])
def list_my_offers(partner: CurrentPartner, db: DbSession):
    return offer_service.list_for_partner(db, partner)


@router.post("/offers", response_model=PartnerOfferOut, status_code=status.HTTP_201_CREATED)
def create_offer(body: OfferCreate, partner: CurrentPartner, db: DbSession):
    return offer_service.create(db, partner, body)


@router.patch("/offers/{offer_id}", response_model=PartnerOfferOut)
def set_offer_status(offer_id: int, body: OfferStatusUpdate, partner: CurrentPartner, db: DbSession):
    return offer_service.set_active(db, partner, offer_id, body.active)
