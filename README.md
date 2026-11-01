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
cp .env.example .env              # konfiguracja (jednorazowo)
docker compose up -d              # baza PostgreSQL
uv sync                           # zależności Pythona
uv run alembic upgrade head       # tabele + konta testowe
uv run fastapi dev app/main.py    # API: http://127.0.0.1:8000/docs
```

Koncepcja systemu: [`docs/VoucherHub_Koncepcja_systemu_v0.2_2026-10-25.pdf`](docs/VoucherHub_Koncepcja_systemu_v0.2_2026-10-25.pdf)
