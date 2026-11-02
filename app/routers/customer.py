from fastapi import APIRouter, status

from app.db import DbSession
from app.models import Voucher
from app.schemas import OfferOut, PurchaseRequest, VoucherOut
from app.services import offers as offer_service
from app.services import vouchers as voucher_service

router = APIRouter(prefix="/api/v1", tags=["customer"])


def _to_voucher_out(voucher: Voucher) -> VoucherOut:
    return VoucherOut(
        code=voucher.code,
        status=voucher_service.display_status(voucher),
        price_paid=voucher.price_paid,
        purchased_at=voucher.purchased_at,
        expires_at=voucher.expires_at,
        redeemed_at=voucher.redeemed_at,
        offer=OfferOut.model_validate(voucher.offer),
    )


@router.get("/offers", response_model=list[OfferOut])
def list_offers(db: DbSession):
    return offer_service.list_available(db)


@router.get("/offers/{offer_id}", response_model=OfferOut)
def get_offer(offer_id: int, db: DbSession):
    return offer_service.get_available(db, offer_id)


@router.post("/offers/{offer_id}/purchase", response_model=VoucherOut, status_code=status.HTTP_201_CREATED)
def purchase_offer(offer_id: int, body: PurchaseRequest, db: DbSession):
    voucher = voucher_service.purchase(db, offer_id, body.email)
    return _to_voucher_out(voucher)


@router.get("/vouchers/{code}", response_model=VoucherOut)
def get_voucher(code: str, db: DbSession):
    return _to_voucher_out(voucher_service.get_by_code(db, code))
