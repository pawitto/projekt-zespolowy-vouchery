from sqlalchemy import Select, select
from sqlalchemy.orm import Session, joinedload

from app.errors import OfferNotAvailable, OfferNotFound
from app.models import Offer, Partner
from app.schemas import OfferCreate


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


def list_for_partner(db: Session, partner: Partner) -> list[Offer]:
    """Wszystkie oferty partnera, także wyłączone (reguła 8: tylko swoje)."""
    stmt = (
        select(Offer)
        .where(Offer.partner_id == partner.id)
        .order_by(Offer.created_at.desc(), Offer.id.desc())
    )
    return list(db.scalars(stmt))


def create(db: Session, partner: Partner, data: OfferCreate) -> Offer:
    offer = Offer(partner_id=partner.id, active=True, **data.model_dump())
    db.add(offer)
    db.commit()
    db.refresh(offer)  # wczytuje created_at nadane przez bazę (DEFAULT now())
    return offer


def set_active(db: Session, partner: Partner, offer_id: int, active: bool) -> Offer:
    offer = db.scalar(select(Offer).where(Offer.id == offer_id, Offer.partner_id == partner.id))
    if offer is None:  # nie istnieje albo należy do innego partnera
        raise OfferNotFound()
    offer.active = active
    db.commit()
    return offer
