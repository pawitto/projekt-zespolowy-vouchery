# projekt-zespolowy-vouchery

Backend systemu **VoucherHub**: partnerzy (siłownie, sauny, SPA) sprzedają vouchery na swoje usługi,
klienci je kupują (płatność symulowana) i realizują u partnera, podając kod `VH-XXXX-XXXX-XXXX`.

**Technologie:** Python 3.14, FastAPI, SQLAlchemy 2.0, Alembic, PostgreSQL 18 (Docker), uv, JWT, argon2.

## Wymagania

- [uv](https://docs.astral.sh/uv/) (instaluje też odpowiednią wersję Pythona)
- Docker z Docker Compose

## Uruchomienie lokalne

```bash
cp .env.example .env              # konfiguracja (jednorazowo), potem ustaw JWT_SECRET (patrz niżej)
docker compose up -d              # baza PostgreSQL
uv sync                           # zależności Pythona
uv run alembic upgrade head       # tabele + konta testowe
uv run fastapi dev app/main.py    # API: http://127.0.0.1:8000/docs
```

### JWT_SECRET

Aplikacja podpisuje tokeny partnerów sekretem z `.env`. Bez `JWT_SECRET` (min. 32 znaki) nie wystartuje.
Wygeneruj własny i wpisz do `.env`:

```bash
uv run python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Po zmianie `.env` zrestartuj aplikację (`Ctrl+C` i ponownie `uv run fastapi dev app/main.py`).

## Konta testowe partnerów

> Tylko do developmentu. Konta tworzy migracja `alembic/versions/a23f7ee903e2_seed_partners.py`.

Szablon: **login = typ partnera, hasło = login + `123`**.

| Partner          | Login      | Hasło         | Aktywny | Uwagi                                              |
|------------------|------------|---------------|---------|----------------------------------------------------|
| Sauna Relax      | `sauna`    | `sauna123`    | tak     |                                                    |
| FitZone Siłownia | `silownia` | `silownia123` | tak     |                                                    |
| Spa Harmonia     | `spa`      | `spa123`      | nie     | do testu: nieaktywny partner nie może się zalogować |

### Logowanie partnera w Swaggerze

1. `POST /api/v1/partner/login` z `{"login": "sauna", "password": "sauna123"}` i skopiuj `access_token`.
2. Kliknij **Authorize** u góry strony i wklej token (bez słowa `Bearer`).
3. Endpointy `/api/v1/partner/...` działają teraz jako zalogowany partner (token ważny 8 h).

## Endpointy

Pełna, interaktywna dokumentacja (Swagger): http://127.0.0.1:8000/docs

🔒 = wymaga nagłówka `Authorization: Bearer <token>`.

| Kto     | Metoda | Endpoint                                  | Opis                                                  |
|---------|--------|-------------------------------------------|-------------------------------------------------------|
| Klient  | GET    | `/api/v1/offers`                          | lista ofert w sprzedaży (z nazwą partnera)            |
| Klient  | GET    | `/api/v1/offers/{id}`                     | szczegóły oferty                                      |
| Klient  | POST   | `/api/v1/offers/{id}/purchase`            | zakup: body `{"email": "..."}` → voucher z kodem (201) |
| Klient  | GET    | `/api/v1/vouchers/{code}`                 | podgląd vouchera po kodzie                            |
| Partner | POST   | `/api/v1/partner/login`                   | logowanie: `{"login", "password"}` → token JWT (8 h)  |
| Partner | GET    | `/api/v1/partner/me`                      | 🔒 dane zalogowanego partnera (poza PDF, dla frontendu) |
| Partner | GET    | `/api/v1/partner/offers`                  | 🔒 moje oferty, także wyłączone                       |
| Partner | POST   | `/api/v1/partner/offers`                  | 🔒 dodanie oferty (201, od razu aktywna)              |
| Partner | PATCH  | `/api/v1/partner/offers/{id}`             | 🔒 włączenie/wyłączenie: body tylko `{"active": bool}` |
| Partner | GET    | `/api/v1/partner/vouchers`                | 🔒 vouchery sprzedane do moich ofert                  |
| Partner | GET    | `/api/v1/partner/vouchers/{code}`         | 🔒 sprawdzenie kodu: usługa, ważność, status          |
| Partner | POST   | `/api/v1/partner/vouchers/{code}/redeem`  | 🔒 realizacja vouchera (ACTIVE → USED)                |
| System  | GET    | `/health`                                 | czy aplikacja i baza działają                         |

Uwagi:
- Kod vouchera można podać małymi literami (`vh-7kq2-...`), API zamienia go na wielkie.
- Ceny są zwracane jako tekst z 2 miejscami po przecinku (`"89.00"`), żeby nie tracić precyzji.
- Daty są w UTC (ISO 8601, sufiks `Z`), frontend przelicza je na czas lokalny.

## Statusy vouchera

| Status    | Znaczenie                         | Skąd                                          |
|-----------|-----------------------------------|-----------------------------------------------|
| `ACTIVE`  | można zrealizować                 | zapisany w bazie                              |
| `USED`    | zrealizowany (`redeemed_at`)      | zapisany w bazie                              |
| `EXPIRED` | minął termin ważności             | **wyliczany** z `expires_at`, nie ma go w bazie |

## Błędy

Błędy biznesowe mają format:

```json
{"detail": "Voucher został już wykorzystany", "code": "VOUCHER_ALREADY_USED"}
```

Frontend powinien rozpoznawać błąd po polu `code` (`detail` to komunikat dla człowieka).

| HTTP | `code`                 | Kiedy                                                        |
|------|------------------------|--------------------------------------------------------------|
| 401  | `INVALID_CREDENTIALS`  | zły login lub hasło                                          |
| 401  | `NOT_AUTHENTICATED`    | brak tokenu w nagłówku `Authorization`                       |
| 401  | `INVALID_TOKEN`        | token nieprawidłowy lub wygasł → trzeba zalogować się ponownie |
| 403  | `PARTNER_INACTIVE`     | konto partnera jest nieaktywne                               |
| 404  | `OFFER_NOT_AVAILABLE`  | (klient) oferta nie istnieje albo nie jest w sprzedaży       |
| 404  | `OFFER_NOT_FOUND`      | (partner) oferta nie istnieje albo należy do innego partnera |
| 404  | `VOUCHER_NOT_FOUND`    | voucher nie istnieje (dla partnera: także cudzy voucher)     |
| 409  | `VOUCHER_ALREADY_USED` | voucher już zrealizowany                                     |
| 409  | `VOUCHER_EXPIRED`      | voucher po terminie ważności                                 |
| 422  | —                      | błąd walidacji danych wejściowych (standard FastAPI: lista błędów w `detail`) |

## Testy

> **TODO:** projekt nie ma jeszcze testów automatycznych, trzeba je dodać (np. `pytest` + `TestClient` z FastAPI).
> Na razie endpointy były sprawdzane ręcznie w Swaggerze.

Koncepcja systemu: [`docs/VoucherHub_Koncepcja_systemu_v0.2_2026-10-25.pdf`](docs/VoucherHub_Koncepcja_systemu_v0.2_2026-10-25.pdf)
