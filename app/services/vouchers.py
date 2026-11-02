import secrets
from datetime import UTC, datetime, timedelta

from sqlalchemy import Select, select
from sqlalchemy.orm import Session, contains_eager, joinedload

from app.errors import VoucherAlreadyUsed, VoucherExpired, VoucherNotFound
from app.models import Offer, Partner, Voucher, VoucherStatus
from app.schemas import VoucherDisplayStatus
from app.services import offers as offer_service

# Bez znaków mylących przy przepisywaniu: 0/O, 1/I/L
CODE_ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"
MAX_CODE_ATTEMPTS = 5


def generate_code() -> str:
    groups = ("".join(secrets.choice(CODE_ALPHABET) for _ in range(4)) for _ in range(3))
    return "VH-" + "-".join(groups)


def normalize_code(code: str) -> str:
    return code.strip().upper()


def display_status(voucher: Voucher, now: datetime | None = None) -> VoucherDisplayStatus:
    """Status dla klienta/recepcji. EXPIRED wyliczamy, nie zapisujemy (PDF, sekcja Dane)."""
    if voucher.status == VoucherStatus.USED:
        return VoucherDisplayStatus.USED
    if (now or datetime.now(UTC)) >= voucher.expires_at:
        return VoucherDisplayStatus.EXPIRED
    return VoucherDisplayStatus.ACTIVE


def purchase(db: Session, offer_id: int, email: str) -> Voucher:
    offer = offer_service.get_available(db, offer_id)  # reguły 1 i 11
    now = datetime.now(UTC)
    voucher = Voucher(
        offer=offer,
        code=_unique_code(db),  # reguła 4
        customer_email=email,
        price_paid=offer.price,  # cena z chwili zakupu
        status=VoucherStatus.ACTIVE,
        purchased_at=now,
        expires_at=now + timedelta(days=offer.validity_days),  # reguła 3
    )
    db.add(voucher)
    db.commit()
    return voucher


def get_by_code(db: Session, code: str) -> Voucher:
    voucher = db.scalar(
        select(Voucher)
        .where(Voucher.code == normalize_code(code))
        .options(joinedload(Voucher.offer).joinedload(Offer.partner))
    )
    if voucher is None:
        raise VoucherNotFound()
    return voucher


def _unique_code(db: Session) -> str:
    for _ in range(MAX_CODE_ATTEMPTS):
        code = generate_code()
        if db.scalar(select(Voucher.id).where(Voucher.code == code)) is None:
            return code
    raise RuntimeError("Nie udało się wygenerować unikalnego kodu")


def _partner_vouchers(partner: Partner) -> Select[tuple[Voucher]]:
    """Vouchery do ofert danego partnera (reguła 8)."""
    return (
        select(Voucher)
        .join(Voucher.offer)
        .where(Offer.partner_id == partner.id)
        .options(contains_eager(Voucher.offer))
    )


def list_for_partner(db: Session, partner: Partner) -> list[Voucher]:
    return list(db.scalars(_partner_vouchers(partner).order_by(Voucher.purchased_at.desc())))


def get_for_partner(db: Session, partner: Partner, code: str) -> Voucher:
    voucher = db.scalar(_partner_vouchers(partner).where(Voucher.code == normalize_code(code)))
    if voucher is None:  # nie istnieje albo należy do innego partnera
        raise VoucherNotFound()
    return voucher


def redeem(db: Session, partner: Partner, code: str) -> Voucher:
    voucher = get_for_partner(db, partner, code)  # reguły 6 i 8
    now = datetime.now(UTC)
    status = display_status(voucher, now)
    if status == VoucherDisplayStatus.USED:  # reguła 5
        raise VoucherAlreadyUsed()
    if status == VoucherDisplayStatus.EXPIRED:  # reguła 7
        raise VoucherExpired()
    voucher.status = VoucherStatus.USED
    voucher.redeemed_at = now
    db.commit()
    return voucher
