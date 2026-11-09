import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Numeric, String, Text, func, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class VoucherStatus(enum.StrEnum):
    """Statusy zapisywane w bazie. 'EXPIRED' nie jest zapisywany, liczymy go z expires_at."""

    ACTIVE = "ACTIVE"
    USED = "USED"


class Partner(Base):
    __tablename__ = "partners"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    login: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    active: Mapped[bool] = mapped_column(default=True, server_default=true())

    offers: Mapped[list["Offer"]] = relationship(back_populates="partner")


class Offer(Base):
    __tablename__ = "offers"
    __table_args__ = (
        CheckConstraint("price > 0", name="price_positive"),
        CheckConstraint("validity_days > 0", name="validity_days_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    partner_id: Mapped[int] = mapped_column(ForeignKey("partners.id"), index=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    validity_days: Mapped[int]
    active: Mapped[bool] = mapped_column(default=True, server_default=true())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    partner: Mapped[Partner] = relationship(back_populates="offers")
    vouchers: Mapped[list["Voucher"]] = relationship(back_populates="offer")


class Voucher(Base):
    __tablename__ = "vouchers"

    id: Mapped[int] = mapped_column(primary_key=True)
    offer_id: Mapped[int] = mapped_column(ForeignKey("offers.id"), index=True)
    code: Mapped[str] = mapped_column(String(20), unique=True)
    customer_email: Mapped[str] = mapped_column(String(320))
    price_paid: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    status: Mapped[VoucherStatus] = mapped_column(
        Enum(VoucherStatus, native_enum=False, create_constraint=True, length=10, name="voucher_status"),
        default=VoucherStatus.ACTIVE,
    )
    purchased_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    redeemed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    offer: Mapped[Offer] = relationship(back_populates="vouchers")
