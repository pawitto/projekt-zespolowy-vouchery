# projekt-zespolowy-vouchery

## Konta testowe partnerów

> Tylko do developmentu. Konta tworzy migracja `alembic/versions/a23f7ee903e2_seed_partners.py`.

Szablon: **login = typ partnera, hasło = login + `123`**.

| Partner          | Login      | Hasło         | Aktywny | Uwagi                                              |
|------------------|------------|---------------|---------|----------------------------------------------------|
| Sauna Relax      | `sauna`    | `sauna123`    | tak     |                                                    |
| FitZone Siłownia | `silownia` | `silownia123` | tak     |                                                    |
| Spa Harmonia     | `spa`      | `spa123`      | nie     | do testu: nieaktywny partner nie może się zalogować |

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

### Logowanie partnera w Swaggerze

1. `POST /api/v1/partner/login` z `{"login": "sauna", "password": "sauna123"}` i skopiuj `access_token`.
2. Kliknij **Authorize** u góry strony i wklej token (bez słowa `Bearer`).
3. Endpointy `/api/v1/partner/...` działają teraz jako zalogowany partner (token ważny 8 h).

Koncepcja systemu: [`docs/VoucherHub_Koncepcja_systemu_v0.2_2026-10-25.pdf`](docs/VoucherHub_Koncepcja_systemu_v0.2_2026-10-25.pdf)
