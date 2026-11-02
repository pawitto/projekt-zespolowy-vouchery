from fastapi import APIRouter

from app.db import DbSession
from app.dependencies import CurrentPartner
from app.schemas import LoginRequest, PartnerMe, TokenResponse
from app.security import create_access_token
from app.services import auth as auth_service

router = APIRouter(prefix="/api/v1/partner", tags=["partner"])


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: DbSession):
    partner = auth_service.authenticate(db, body.login, body.password)
    token, expires_at = create_access_token(partner.id)
    return TokenResponse(access_token=token, expires_at=expires_at)


@router.get("/me", response_model=PartnerMe)
def me(partner: CurrentPartner):
    return partner
