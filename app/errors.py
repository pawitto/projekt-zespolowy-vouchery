class DomainError(Exception):
    """Bazowy błąd biznesowy: status HTTP + kod dla frontendu + komunikat."""

    status_code: int = 400
    code: str = "DOMAIN_ERROR"
    message: str = "Błąd operacji"
    headers: dict[str, str] | None = None  # dodatkowe nagłówki HTTP odpowiedzi

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


_BEARER = {"WWW-Authenticate": "Bearer"}


class InvalidCredentials(DomainError):
    status_code = 401
    code = "INVALID_CREDENTIALS"
    message = "Nieprawidłowy login lub hasło"


class PartnerInactive(DomainError):
    status_code = 403
    code = "PARTNER_INACTIVE"
    message = "Konto partnera jest nieaktywne"


class NotAuthenticated(DomainError):
    status_code = 401
    code = "NOT_AUTHENTICATED"
    message = "Brak tokenu. Zaloguj się."
    headers = _BEARER


class InvalidToken(DomainError):
    status_code = 401
    code = "INVALID_TOKEN"
    message = "Token jest nieprawidłowy lub wygasł. Zaloguj się ponownie."
    headers = _BEARER
