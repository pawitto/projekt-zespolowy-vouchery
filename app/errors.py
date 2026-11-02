class DomainError(Exception):
    """Bazowy błąd biznesowy: status HTTP + kod dla frontendu + komunikat."""

    status_code: int = 400
    code: str = "DOMAIN_ERROR"
    message: str = "Błąd operacji"

    def __init__(self, message: str | None = None):
        super().__init__(message or self.message)
        self.message = message or self.message


class OfferNotAvailable(DomainError):
    status_code = 404
    code = "OFFER_NOT_AVAILABLE"
    message = "Oferta nie istnieje lub nie jest dostępna"


class VoucherNotFound(DomainError):
    status_code = 404
    code = "VOUCHER_NOT_FOUND"
    message = "Voucher o podanym kodzie nie istnieje"
