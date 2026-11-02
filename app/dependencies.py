from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.db import DbSession
from app.errors import InvalidToken, NotAuthenticated, PartnerInactive
from app.models import Partner
from app.security import TokenError, decode_access_token

bearer_scheme = HTTPBearer(auto_error=False, description="Token z POST /api/v1/partner/login")


def get_current_partner(
    db: DbSession,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> Partner:
    if credentials is None:
        raise NotAuthenticated()
    try:
        partner_id = decode_access_token(credentials.credentials)
    except TokenError:
        raise InvalidToken() from None
    partner = db.get(Partner, partner_id)
    if partner is None:
        raise InvalidToken()
    if not partner.active:  # PDF: sprawdzamy przy każdym zapytaniu
        raise PartnerInactive()
    return partner


CurrentPartner = Annotated[Partner, Depends(get_current_partner)]
