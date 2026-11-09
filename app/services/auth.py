from sqlalchemy import select
from sqlalchemy.orm import Session

from app.errors import InvalidCredentials, PartnerInactive
from app.models import Partner
from app.security import hash_password, verify_password

# Hash "na pusto", żeby nieistniejący login trwał tyle samo co zły login + hasło
_DUMMY_HASH = hash_password("dummy-password-for-timing")


def authenticate(db: Session, login: str, password: str) -> Partner:
    partner = db.scalar(select(Partner).where(Partner.login == login))
    if partner is None:
        verify_password(password, _DUMMY_HASH)
        raise InvalidCredentials()
    if not verify_password(password, partner.password_hash):
        raise InvalidCredentials()
    if not partner.active:  # reguła 11
        raise PartnerInactive()
    return partner
