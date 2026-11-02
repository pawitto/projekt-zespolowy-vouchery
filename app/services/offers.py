from sqlalchemy import Select, select
from sqlalchemy.orm import Session, joinedload

from app.errors import OfferNotAvailable
from app.models import Offer, Partner


def _available_offers() -> Select[tuple[Offer]]:
    """Oferty w sprzedaży: aktywna oferta aktywnego partnera (reguły 1 i 11)."""
    return (
        select(Offer)
        .join(Offer.partner)
        .where(Offer.active.is_(True), Partner.active.is_(True))
        .options(joinedload(Offer.partner))
    )


def list_available(db: Session) -> list[Offer]:
    return list(db.scalars(_available_offers().order_by(Offer.created_at.desc())))


def get_available(db: Session, offer_id: int) -> Offer:
    offer = db.scalar(_available_offers().where(Offer.id == offer_id))
    if offer is None:
        raise OfferNotAvailable()
    return offer
