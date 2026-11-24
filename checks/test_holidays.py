"""Checkpoint "holidays": public holidays from the `holidays` package (check K13, canvas block 8).

Run all checks with:  uv run pytest checks
"""

import bakery_holidays as hol
import invariants as inv


def test_k13_public_holidays(sales):
    public_holidays = hol.public_holidays_sh(inv.FIRST_DATE, inv.LAST_DATE)
    inv.check_public_holidays(public_holidays, sales)
