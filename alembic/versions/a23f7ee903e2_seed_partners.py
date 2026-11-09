"""seed partners

Revision ID: a23f7ee903e2
Revises: 04d3a9e544b7
Create Date: 2026-11-01 19:48:34.754116

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a23f7ee903e2'
down_revision: Union[str, Sequence[str], None] = '04d3a9e544b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Konta testowe (TYLKO DEV), szablon: login = typ partnera, hasło = login + "123".
# Hashe argon2 wygenerowane przez app.security.hash_password; jawne hasła są w README.md.
# Lokalny opis tabeli zamiast importu app.models: migracja nie zależy od przyszłych zmian modeli.
partners = sa.table(
    "partners",
    sa.column("name", sa.String),
    sa.column("login", sa.String),
    sa.column("password_hash", sa.String),
    sa.column("active", sa.Boolean),
)

SEED_LOGINS = ("sauna", "silownia", "spa")


def upgrade() -> None:
    """Dodaje 3 partnerów testowych (jeden nieaktywny)."""
    op.bulk_insert(
        partners,
        [
            {
                "name": "Sauna Relax",
                "login": "sauna",  # hasło: sauna123
                "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$9SJKSrFlBKSy51yzu+xitg$Themmqfr278Cz8g3WuL7opBxgWklMWENP3o1q8JUX0A",
                "active": True,
            },
            {
                "name": "FitZone Siłownia",
                "login": "silownia",  # hasło: silownia123
                "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$WSbvOk6VPMwsfyUGq+LAmA$P9ECZ7Z3Fdd/9luF1H/JOJJddBOifH2szNtW6J0LrbM",
                "active": True,
            },
            {
                "name": "Spa Harmonia",
                "login": "spa",  # hasło: spa123
                "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$R6rYVNCqH2ckaRXOxTIa+A$1CwnlX6s160SHzz79P5j52nfCVIzk67apgdTfQuP3rA",
                "active": False,
            },
        ],
    )


def downgrade() -> None:
    """Usuwa partnerów testowych."""
    op.execute(partners.delete().where(partners.c.login.in_(SEED_LOGINS)))
